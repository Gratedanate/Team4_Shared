import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Team 4 Final Dashboard"
)
server = app.server  # for deployment

app.layout = html.Div(
    className="page-wrapper",
    children=[
        # Navbar
        dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("Team 4 Final Dashboard", className="brand-text"),

                # Centered nav links
                dbc.Nav(
                    [
                        dbc.NavLink("About", href="/", active="exact"),
                        dbc.NavLink("Bank Closures Map", href="/pageone", active="exact"),
                        dbc.NavLink("Trend Comparison", href="/pagetwo", active="exact"),
                    ],
                    className="nav-links"
                ),
            ], fluid=True),
            className="custom-navbar",
            dark=True
        ),

        # Page content container
        html.Div(dash.page_container, className="page-content"),

        # Footer
        html.Footer("Zoe Zung | Brynn Vetrano | Nathan Brewer | Data from FDIC & Federal Reserve", className="footer")
    ]
)

if __name__ == "__main__":
    app.run(debug=True)