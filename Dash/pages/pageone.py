import dash
from dash import html

dash.register_page(__name__, path="/pageone", name = "Page 1")

layout = html.Div([
    html.H2("Welcome to my Page 1"),
    html.P("This is a simple multipage Dash project example.")
])