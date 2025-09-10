import dash 
from dash import html, dcc, Input, Output, callback, register_page 
import pandas as pd 
import plotly.express as px 
from pathlib import Path

register_page(__name__, path="/pagetwo", name="Trend Comparison")

# --- Load Data ---
DataPath_failures = Path(__file__).resolve().parent.parent / "data" / "banks.csv"
DataPath_rates = Path(__file__).resolve().parent.parent / "data" / "yield-curve-rates-1990-2024.csv"

failures = pd.read_csv(DataPath_failures)
rates = pd.read_csv(DataPath_rates)

failures["Closing Date"] = pd.to_datetime(failures["Closing Date"], format="%d-%b-%y")
failures["Year"] = failures["Closing Date"].dt.year
failures_by_year = failures.groupby("Year").size().rename("Bank Failures")

rates["Date"] = pd.to_datetime(rates["Date"], format="%m/%d/%y")
rates["Year"] = rates["Date"].dt.year
avg_rates_by_year = rates.groupby("Year")[["10 Yr", "1 Mo"]].mean()
avg_rates_by_year["Spread (10 Yr - 1 M)"] = avg_rates_by_year["10 Yr"] - avg_rates_by_year["1 Mo"]

merged = pd.merge(failures_by_year, avg_rates_by_year, left_index=True, right_index=True).reset_index()
merged = merged[merged["Year"] >= 2007]
merged["Interest Rate Spread"] = merged["Spread (10 Yr - 1 M)"].map(lambda x: f"{x:.2f}%")

# --- Layout ---
layout = html.Div(
    children=[
        html.H1("Bank Failures vs. Treasury Yield Spread", style={"textAlign": "center", "marginBottom": "20px"}),

        # Dropdown in card
        html.Div(
            className="card",
            children=[
                html.Label("Select Data View:"),
                dcc.Dropdown(
                    id="data-view-selector",
                    options=[
                        {"label": "Bank Failures Only", "value": "failures"},
                        {"label": "Yield Spread Only", "value": "spread"},
                        {"label": "Both", "value": "both"},
                    ],
                    value="both",
                    clearable=False,
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Graph in card
        html.Div(
            className="card",
            children=[
                dcc.Graph(id="bank-failure-graph"),
                html.P(
                    "Hover over the bars/line to see yearly details.",
                    style={
                        "color": "#7a8a80",      # muted grey-green (same as subtitle color)
                        "fontStyle": "italic",  # italicized
                        "marginTop": "10px",
                        "textAlign": "left",
                    },
                ),
            ],
        ),

        # Pill button
        html.Div(
            id="show-blurb-button-container",
            children=[
                html.Button(
                    "Show Yield Spread Info",
                    id="show-blurb-button",
                    n_clicks=0,
                    className="pill-button",  # styled like nav buttons
                )
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),

        # Yield info (appears in card when toggled)
        html.Div(id="yield-spread-info", style={"marginTop": "20px"}),
    ]
)

# --- Callbacks ---
@callback(
    Output("bank-failure-graph", "figure"),
    Input("data-view-selector", "value"),
)
def update_graph(view_choice):
    filtered_data = merged[merged["Year"] >= 2007]
    if view_choice == "failures":
        fig = px.bar(
            filtered_data,
            x="Year",
            y="Bank Failures",
            labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
            title="Bank Failures by Year",
            color_discrete_sequence=["#90a997"],
        )

    elif view_choice == "spread":
        fig = px.line(
            filtered_data,
            x="Year",
            y="Spread (10 Yr - 1 M)",
            labels={"Year": "Year", "Spread (10 Yr - 1 M)": "Yield Spread (%)"},
            title="Yield Spread (10 Yr - 1 Mo) by Year",
            color_discrete_sequence=["#2c3e50"],
        )

    else:  
        fig = px.bar(
            filtered_data,
            x="Year",
            y="Bank Failures",
            labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
            title="Bank Failures and Yield Spread (10 Yr - 1 Mo) by Year",
            color_discrete_sequence=["#90a997"],
        )

        fig.add_scatter(
            x=filtered_data["Year"],
            y=filtered_data["Interest Rate Spread"].str.rstrip('%').astype(float),
            mode="lines",
            name="Spread (%)",
            yaxis="y2",
            line=dict(color="#2c3e50", width=2),
            showlegend=False,
        )

        fig.update_layout(
            yaxis=dict(title="Bank Failures"),
            yaxis2=dict(
                title="Yield Spread (%)",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
        )

    fig.update_layout(
        xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False),
        plot_bgcolor="#f5f7f4",
        paper_bgcolor="#ffffff",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified",
    )
    return fig


@callback(
    Output("yield-spread-info", "children"),
    Input("show-blurb-button", "n_clicks"),
)
def display_blurb(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return html.Div(
            className="card",
            children=[
                html.P(
                    """
                    The yield spread, which is the difference between long-term and short-term interest rates, 
                    is closely watched as an economic indicator and has a direct connection to the banking sector’s health. 
                    During normal economic conditions, a positive yield spread means banks can profitably borrow short-term 
                    funds and lend at higher long-term rates. However, when the yield curve flattens or inverts, as it did 
                    before the Great Recession, this profitability margin shrinks or disappears.
                    """
                ),
                html.P(
                    """
                    Leading up to the 2007-2009 financial crisis, the yield spread significantly narrowed and even inverted. 
                    This put tremendous pressure on banks’ earnings because their traditional business model became less viable. 
                    Reduced profitability made banks more vulnerable to loan losses and liquidity issues, contributing to a wave 
                    of bank failures during the Great Recession.
                    """
                ),
                html.P(
                    """
                    So, the yield spread serves not only as a predictor of economic slowdowns but also as a critical warning sign 
                    for banking sector stress and potential failures. Monitoring this spread helps policymakers, investors, and 
                    banks themselves anticipate and respond to financial instability.
                    """
                ),
            ],
        )
    return ""