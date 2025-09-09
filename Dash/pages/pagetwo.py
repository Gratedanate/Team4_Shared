import dash
from dash import html

dash.register_page(__name__, path="/pagetwo", name = "Page 2")

layout = html.Div([
    html.H2("Welcome to my Page 2"),
    html.P("This is a simple multipage Dash project example.")
])