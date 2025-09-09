from dash import html, dcc, callback, register_page, Output, Input
import pandas as pd
import plotly.express as px
from pathlib import Path

register_page(__name__, path="/pageone", name = "Page 1")

data = Path(__file__).resolve().parent.parent / "data" / "banks.csv"

df = pd.read_csv(data, encoding='latin1')

df.columns = df.columns.str.strip()
df['upd_ClosingDate'] = pd.to_datetime(df["Closing Date"], format="%d-%b-%y")
df["year"] = df["upd_ClosingDate"].dt.year
closures = df.groupby(["year", "State"]).size().reset_index(name="closures")


layout = html.Div([
    html.H1("Bank Closure Data since 2000"),
    dcc.Slider(
        id="slider",
        min=(closures["year"].min()),
        max=(closures["year"].max()),
        value=(closures["year"].min()),
        marks={str(y): str(y) for y in sorted(closures["year"].unique())},
        step=None,
    ),
    dcc.Graph(id="map"),
])

@callback(
    Output("map", "figure"),
    Input("slider", "value")
)

def bank_map(selected_year):
    d = closures[closures["year"] == selected_year]
    fig = px.choropleth(
        d, 
        title = f"Bank Closures in the US - {selected_year}",
        labels = {"color": "Number of Closures"},
        locations = "State",
        locationmode = "USA-states",
        scope ="usa",
        color = "closures",
        color_continuous_scale = "greens",
    )

    return fig