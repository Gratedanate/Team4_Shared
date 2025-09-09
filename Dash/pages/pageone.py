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
    html.H1("Bank Closure Data since 2007"),
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
        ], style={"flex": "3", "padding": "10px", "height": "600px"}),
        html.Div([
            dcc.Dropdown(
                id="state-dropdown",
                options=[{"label": n, "value": n} for n in sorted(closures["State"].unique())]
            ),
            html.Div(id="state-info", ),
        ], style={"flex": "1", "padding": "10px"}),
    ], style={"display": "flex", "flex-direction": "row", "align-items": "stretch"}),
])

@callback(
    Output("map", "figure"),
    Output("state-info", "children"),
    Input("slider", "value"),
    Input("state-dropdown", "value"),
)

def unified_functions(selected_year, selected_state):
    d = closures[closures["year"] == selected_year]
    fig = px.choropleth(
        d, 
        title = f"Bank Closures in the US - {selected_year}",
        labels = {"color": "Number of Closures"},
        locations = "State",
        locationmode = "USA-states",
        scope ="usa",
        color = "closures",
        color_continuous_scale = ["#f5f7f4", "#90a997", "#2c3e50"],
    )

    if not selected_state:
        info = "Select a state to learn more."
    else:    
        state_data = df[(df["State"] == selected_state) & (df["year"] == selected_year)]
        
        if state_data.empty: 
            info = f"No bank closures in {selected_state} during {selected_year}."
        else:
            closed_banks = []
            for index, row in state_data.iterrows():
                closed_banks.append(html.Li(
                f"{row['Bank Name']}, "
                f"- Closed {row['upd_ClosingDate'] :%B %d, %Y}, "
                f"- Acquiring Institution: {row['Acquiring Institution']}"
                ))

            info = html.Div([
                html.H3(f"Bank Closures in {selected_state}, during {selected_year}:"),
                html.Ul(closed_banks)
            ])

    return fig, info