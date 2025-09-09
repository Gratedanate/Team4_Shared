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

    html.P("Hover over the bars/line to see yearly details.")
])


@callback(
    Output("bank-failure-graph", "figure"),
    Input("data-view-selector", "value")
)
def update_graph(view_choice):
    filtered_data = merged[merged["Year"] > 2007]

    if view_choice == "failures":
        fig = px.bar(
            filtered_data,
            x="Year",
            y="Bank Failures",
            labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
            title="Bank Failures by Year"
        )

    elif view_choice == "spread":
        fig = px.line(
            filtered_data,
            x="Year",
            y="Spread (10 Yr - 1 M)",
            labels={"Year": "Year", "Spread (10 Yr - 1 M)": "Yield Spread (%)"},
            title="Yield Spread (10 Yr - 1 Mo) by Year"
        )

    else:  
        fig = px.bar(
            filtered_data,
            x="Year",
            y="Bank Failures",
            labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
            title="Bank Failures and Yield Spread (10 Yr - 1 Mo) by Year",
            hover_data={"Spread (10 Yr - 1 M)": ':.2', "Bank Failures": True}
        )

        fig.add_scatter(
            x=filtered_data["Year"],
            y=filtered_data["Spread (10 Yr - 1 M)"],
            mode="lines",
            name="Spread (10 Yr - 1 Mo)",
            yaxis="y2",
            line=dict(color="orange", width=2),
            hoverinfo="skip",
        )

        fig.update_layout(
            yaxis=dict(title="Bank Failures"),
            yaxis2=dict(
                title="Yield Spread (%)",
                overlaying="y",
                side="right",
                showgrid=False,
            )
        )

    fig.update_layout(
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=1,
            tickangle=0
        ),
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
    )

    return fig
