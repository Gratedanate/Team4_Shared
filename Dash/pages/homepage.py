import dash
from dash import html

dash.register_page(__name__, path="/", name="Home")

layout = html.Div(
    style={
        "maxWidth": "800px",
        "margin": "0 auto",
        "padding": "40px",
        "fontFamily": "Arial, sans-serif",
        "lineHeight": "1.6",
    },
    children=[
        html.H1(
            "Failed US Banks & Interest Rates",
            style={
                "textAlign": "center",
                "marginBottom": "20px",
                "color": "#2c3e50",
            },
        ),
        html.H3(
            "Exploring Financial Stability and Policy Impacts",
            style={
                "textAlign": "center",
                "marginBottom": "40px",
                "fontWeight": "normal",
                "color": "#34495e",
            },
        ),
        html.P(
            """
            This dashboard examines the relationship between failed US banks over recent years 
            and changes in US interest rates. By combining historical data on bank closures 
            with Federal Reserve yield curve rates, we aim to uncover patterns that highlight 
            how monetary policy may influence financial stability.
            """
        ),
        html.P(
            """
            Our goal is to provide an accessible, data-driven overview of these trends, 
            offering insights for students, researchers, and anyone curious about the 
            intersection of banking health and interest rate policy.
            """
        ),
        html.P(
            """
            Use the navigation menu to explore interactive charts, trends over time, 
            and comparisons between bank failures and interest rate movements.
            """
        ),
    ],
)

