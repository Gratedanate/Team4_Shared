import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H2("US Census Data"),
    html.P("[Description of the Dashboard]")
])  
