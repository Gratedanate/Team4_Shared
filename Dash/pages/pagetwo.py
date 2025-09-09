import dash
from dash import html, dcc, Input, Output, callback, register_page
import pandas as pd
import plotly.express as px
from pathlib import Path


register_page(__name__, path="/pagetwo", name = "Page 2")

layout = html.Div([
    html.H2("Welcome to my Page 2"),
    html.P("This is a simple multipage Dash project example.")
])

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

fig = px.bar(
    merged,
    x="Year",
    y="Bank Failures",
    labels={"Year": "Year", "Bank Failures": "Number of Bank Failures"},
    title="Bank Failures and Interest Rate Spread (10 Yr - 1 Mo) by Year",
    hover_data={"Spread (10 Yr - 1 M)": ':.2', "Bank Failures": True},
)

fig.add_scatter(
    x=merged["Year"],
    y=merged["Spread (10 Yr - 1 M)"],
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
    ),
    xaxis= dict(
        title="Year",
        tickmode="linear",
        dtick=1
    ),
        legend=dict(x=0.01, y=0.99),
        hovermode="x unified"
)

layout = html.Div([
    html.H2("Bank Failures vs. Treasury Yield Spread"),
    dcc.Graph(figure=fig),
    html.P("Hover over the bars/line to see yearly details.")
])

