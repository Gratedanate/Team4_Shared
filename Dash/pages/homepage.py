import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    className="page-content home-page",  # ⬅️ added "home-page" for CSS targeting
    children=[
        # Title + Subtitle floating outside the card
        html.Div(
            className="page-header",
            children=[
                html.H1("Failed US Banks & Interest Rates", className="page-title"),
                html.H3("Exploring Financial Stability and Policy Impacts", className="page-subtitle"),
            ]
        ),

        # Main content inside card
        html.Div(
            className="card",
            children=[
                html.P(
                    """
                    This dashboard examines the relationship between failed US banks over recent years 
                    and changes in US interest rates. By combining historical data from FDIC on bank
                    closures with Federal Reserve yield curve rates, we aim to uncover patterns that
                    highlight how monetary policy may influence financial stability.
                    """
                ),
                html.P(
                    """
                    Our goal is to provide an accessible, data-driven overview of these trends, 
                    offering insights about the intersection of banking health and interest rate policy.
                    """
                ),
                html.P(
                    """
                    Click through our pages to explore the interactive map, trends over time, 
                    and comparisons between bank failures and interest rate movements.
                    """
                ),
            ]
        ),
    ]
)
