from dash import html, dcc, callback, register_page, Output, Input, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pathlib import Path
import us

register_page(__name__, path="/pageone", name = "Page 1")

data = Path(__file__).resolve().parent.parent / "data" / "banks.csv"

df = pd.read_csv(data, encoding='latin1')

df.columns = df.columns.str.strip()
df['upd_ClosingDate'] = pd.to_datetime(df["Closing Date"], format="%d-%b-%y")
df["year"] = df["upd_ClosingDate"].dt.year
closures = df.groupby(["year", "State"]).size().reset_index(name="closures")

layout = html.Div([
    html.H1("Bank Closure Data (2007-2025)", style ={"textAlign":"center"}),
    dbc.Row([
        dbc.Col(
            dcc.Slider(
                id="slider",
                min=2007,
                max=(closures["year"].max()),
                value=2007,
                marks={str(y): str(y) for y in sorted(closures["year"].unique())},
                step=None,
            ), 
            width=12, 
            style={"padding":"10px"}
        )
    ]), 
        
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id="map",
                        style = {"height":"450px", "width": "100%", "padding":"10px"}
                    )
                )
            ),
            width = 8
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    dcc.Dropdown(
                        id="state-dropdown",
                        placeholder = "Search for a state to learn more.",
                        options=[{"label": us.states.lookup(n).name, "value": n} for n in sorted(closures["State"].unique())],
                        style={"width": "100%"}
                    )  
                )    
            ], style={"margin-bottom":"10px"}),
            
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.Div(id="bank-info") 
                ])    
            ], style={ "overflowY": "auto", "overflowX": "auto" })),
        ], width=4, style={"padding": "10px"}),
    ])
])

@callback(
    Output("map", "figure"),
    Output("bank-info", "children"),
    Input("slider", "value"),
    Input("state-dropdown", "value"),
)

def unified_function(selected_year, selected_state):
    d = closures[closures["year"] == selected_year]
    fig = px.choropleth(
        d, 
        labels = {"color": "Number of Closures"},
        locations = "State",
        locationmode = "USA-states",
        scope ="usa",
        color = "closures",
        color_continuous_scale = ["#f5f7f4", "#90a997", "#2c3e50"],
    )

    if not selected_state:
        info = None
    else:    
        state_data = df[(df["State"] == selected_state) & (df["year"] == selected_year)]
        
        if state_data.empty: 
            info = f"No bank closures in {us.states.lookup(selected_state).name} during {selected_year}."
        else:
            info = dash_table.DataTable(
                columns=[
                    {"name": "City", "id": "City"},
                    {"name": "Bank Name", "id": "Bank Name"},
                    {"name": "Closing Date", "id": "Closing Date"},
                    {"name": "Acquiring Institution", "id": "Acquiring Institution"},
                ],
                data=[
                    {
                    "City": row["City"],
                    "Bank Name": row["Bank Name"],
                    "Closing Date": row['upd_ClosingDate'].strftime("%B %d, %Y"),
                    "Acquiring Institution": row['Acquiring Institution']
                    }
                    for index, row in state_data.iterrows()
                ],
                style_table={"height": "99%", "overflowY":"auto", "overflowX":"auto"},
                style_header={"fontWeight": "bold"},
                style_cell={"textAlign": "left", "padding": "5px"}
            )

    return fig, info