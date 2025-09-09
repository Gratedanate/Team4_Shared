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
    html.Div([
        html.Div([
            dcc.Slider(
                id="slider",
                min=(closures["year"].min()),
                max=(closures["year"].max()),
                value=(closures["year"].min()),
                marks={str(y): str(y) for y in sorted(closures["year"].unique())},
                step=None,
            ),
            dcc.Graph(id="map"),
        ], style={"flex": "1", "padding": "10px"}),
        html.Div([
            dcc.Dropdown(
                id="state-dropdown",
                options=[{"label": n, "value": n} for n in sorted(closures["State"].unique())]
            ),
            html.Div(id="state-info", style={"padding": "10px"
            }),
        ], style={"flex": "1", "padding": "10px"}),
    ], style={"display": "flex", "flex-direction": "row"}),
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

@callback(
    Output("state-info", "children"),
    [Input("state-dropdown", "value"), Input("slider", "value")]
)

def state_info(selected_state, selected_year):
    if not selected_state:
        return "Select a state to learn more."

    state_data = data[(data["State"] == selected_state) & (data["year"] == selected_year)]

    if state_data.empty(): 
        return f"No bank closures in {selected_state} for {selected_year}."

    closed_banks = []
    for index, row in state_data.iterrows():
        closed_banks.append(html.Li(
            f"{row['Bank Name']}, "
            f"- Closed {row['upd_ClosingDate'] :%B %d, %Y}, "
            f"- Acquiring Institution: {row['Acquiring Institution']}"
        ))

    return html.Div([
        html.H3(f"Bank Closures in {selected_state}, during {selected_year}:"),
        html.Ul(closed_banks)
    ])