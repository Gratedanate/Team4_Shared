import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

##initialize the app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, title = "Multi-Page-App")
server = app.server ## for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Home", href="/", active ="exact"),
            dbc.NavLink("Page 1", href="/pageone", active ="exact"),
            dbc.NavLink("Page 2", href="/pagetwo", active ="exact"),
        ],
    brand = "Multiple Page Census App"),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)