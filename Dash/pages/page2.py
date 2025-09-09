import dash 
from dash import html, dcc, Input, Output, callback, register_page 
import pandas as pd 
import plotly.express as px 
from pathlib import Path

register_page(__name__, path="/pagetwo", name = "Page 2")

DataPath_failures = Path(__file__).resolve().parent.parent / "data" / "banks.csv"
DataPath_rates = Path(__file__).resolve().parent.parent / "data" / "yield-curve-rates-1990-2024.csv"

failures = pd.read_csv(DataPath_failures)
rates = pd.read_csv(DataPath_rates)

failures["Closing Date"] = pd.to_datetime(failures["Closing Date"], format = "%d-%b-%y")
failures["Year"] = failures['Closing Date'].dt.year

failures_by_year = failures.groupby("Year").size().rename("Bank Failures")

rates["Date"] = pd.to_datetime(rates["Date"], format="%m/%d/%y")
rates["Year"] = rates["Date"].dt.year

avg_rates_by_year = rates.groupby("Year")[["10 Yr", "1 Mo"]].mean()
avg_rates_by_year["Spread (10 Yr - 1 M)"] = avg_rates_by_year["10 Yr"] - avg_rates_by_year["1 Mo"]

merged = pd.merge(failures_by_year, avg_rates_by_year, left_index=True, right_index=True).reset_index()
merged = merged[merged["Year"] >= 2007]
merged["Interest Rate Spread"] = merged["Spread (10 Yr - 1 M)"].map(lambda x: f"{x:.2f}%")

layout = html.Div([
    html.H2("Bank Failures vs. Treasury Yield Spread"),

    html.Label("Select Data View:"),
    dcc.Dropdown(
        id="data-view-selector",
        options=[
            {"label": "Bank Failures Only", "value": "failures"},
            {"label": "Yield Spread Only", "value": "spread"},
            {"label": "Both", "value": "both"},
        ],
        value="both",  # default view
        clearable=False
    ),

    dcc.Graph(id="bank-failure-graph"),

    html.P("Hover over the bars/line to see yearly details."),
    html.Div(id="show-blurb-button-container", children=[
        html.Button("Why is the Yield Spread Important?", id="show-blurb-button", n_clicks=0)
    ]),
    html.Div(id="yield-spread-info", style={"marginTop": "20px"})
])


@callback(
    Output("bank-failure-graph", "figure"),
    Input("data-view-selector", "value")
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
            hover_data={"Spread (10 Yr - 1 M)": False, "Interest Rate Spread": False, "Bank Failures": True, "Year": False},
            color_discrete_sequence=["#90a997"]
        )


    elif view_choice == "spread":
        fig = px.line(
            filtered_data,
            x="Year",
            y="Spread (10 Yr - 1 M)",
            labels={"Year": "Year", "Spread (10 Yr - 1 M)": "Yield Spread (%)"},
            title="Yield Spread (10 Yr - 1 Mo) by Year",
            hover_data={"Spread (10 Yr - 1 M)": False, "Interest Rate Spread": True, "Bank Failures": False, "Year": False},
            color_discrete_sequence=["#2c3e50"]
        )

    else:  
        fig = px.bar(
            filtered_data,
            x="Year",
            y="Bank Failures",
            labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
            title="Bank Failures and Yield Spread (10 Yr - 1 Mo) by Year",
            hover_data={"Spread (10 Yr - 1 M)": False, "Interest Rate Spread": False, "Bank Failures": True, "Year": False},
            color_discrete_sequence=["#90a997"]
        )


        fig.add_scatter(
            x=filtered_data["Year"],
            y=filtered_data["Interest Rate Spread"].str.rstrip('%').astype(float),
            mode="lines",
            name="Spread (%)",
            yaxis="y2",
            line=dict(color="#2c3e50", width=2),
            showlegend=False
        )


        fig.update_layout(
            yaxis=dict(title="Bank Failures"),
            yaxis2=dict(
                title="Yield Spread (%)",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            plot_bgcolor="#f5f7f4",
            paper_bgcolor="#ffffff"
        )

    fig.update_layout(
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            tickangle=0,
            showgrid=False
        ),
        plot_bgcolor="#f5f7f4",
        paper_bgcolor="#ffffff",
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )

    return fig

@callback(
    Output("yield-spread-info", "children"),
    Input("show-blurb-button", "n_clicks"),
    Input("data-view-selector", "value")
)

def display_blurb(n_clicks, selected_view):
    if n_clicks and selected_view in ["spread", "both"] and n_clicks % 2 == 1: 
        return (
            """
            The yield spread, which is the difference between long-term and short-term interest rates, is closely watched as an economic indicator and has a direct connection to the banking sector’s health. 
            During normal economic conditions, a positive yield spread means banks can profitably borrow short-term funds and lend at higher long-term rates. 
            However, when the yield curve flattens or inverts, as it did before the Great Recession, this profitability margin shrinks or disappears.

            Leading up to the 2007-2009 financial crisis, the yield spread significantly narrowed and even inverted. 
            This put tremendous pressure on banks’ earnings because their traditional business model became less viable. 
            Reduced profitability made banks more vulnerable to loan losses and liquidity issues, contributing to a wave of bank failures during the Great Recession.

            So, the yield spread serves not only as a predictor of economic slowdowns but also as a critical warning sign for banking sector stress and potential failures. 
            Monitoring this spread helps policymakers, investors, and banks themselves anticipate and respond to financial instability.
            """
            )
    else:
        return "" 

@callback(
    Output("show-blurb-button-container", "style"),
    Input("data-view-selector", "value")
)

def toggle_button_visibility(selected_view):
    if selected_view == "failures":
        return {"display": "none"}
    return {"display": "block"}
