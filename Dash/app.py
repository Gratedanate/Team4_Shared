# AI Usage Appendix:
# Tools Used: CoPilot and ChatGPT
# CoPilot was used for auto filling parts of the code. 
# ChatGPT was used for clarifying code snippets (what the lines meant/did) and changing some of the format of the graphs (for example, editing the hover box on the bank failures graph). Additionally, our team utilized ChatGPT for lists of arguments related to specific functions, information on packages that could simplify coding workflow, and for questions regarding design elements. However, our most significant usage of ChatGPT was for help with the GitHub Repository and understanding how to push and pull code from it.
# What was verified/ edited:
# •	Clarification and layout changes on some of the functions
# •	Verifying the dropdown option of the graphs on page two and editing the button
# •	Design.css file suggestions


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
