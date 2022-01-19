# Done by Muhammad Mustaffa
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_app.layout import nav_buttons, navigation_layout, analysis_layout
from dash_app.callback import dash_callback

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"


def navigation_dash(flask_app):
    """Create a Plotly Dash dashboard"""
    dash_app = dash.Dash(server=flask_app, title='Navigation', assets_folder='../dash_app/assets',
                         routes_pathname_prefix="/navigation_dash/",
                         external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

    ## Creating the app layout
    dash_app.layout = html.Div(id='page_content', children=[
        html.Header(nav_buttons()),
        html.Main(navigation_layout()),
    ])
    dash_callback(dash_app)
    return dash_app.server


def analysis_dash(flask_app):
    """Create a Plotly Dash dashboard"""
    dash_app = dash.Dash(server=flask_app, title='Analysis', assets_folder='../dash_app/assets',
                         routes_pathname_prefix="/analysis_dash/",
                         external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

    ## Creating the app layout
    dash_app.layout = html.Div(id='page_content', children=[
        html.Div(id='analysis_page'),
        html.Header(nav_buttons()),
        html.Main(analysis_layout()),
    ])
    dash_callback(dash_app)
    return dash_app.server
