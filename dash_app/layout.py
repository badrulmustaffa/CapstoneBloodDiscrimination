# Done by Muhammad Mustaffa

import base64
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def logo():
    image_filename = '../my_app/static/img/SarahSquad.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return encoded_image


def nav_buttons():
    """ return the navbar based on the current user status"""
    search_button = html.Form(className="d-flex", id="search_form",
                              children=[
                                  dbc.Input(id='search_input', className="me-2",
                                            placeholder="Type in username"),
                                  dbc.Button("Search", id="search_button", color='success', outline=True,
                                             external_link=True, type='submit',
                                             style={'margin-left': 8})])

    nav_buttons = html.Div(className="navbar-collapse",
                           children=[
                               html.Ul(className="navbar-nav", children=[
                                   html.Li(className="nav-item", children=[
                                       html.A(className="nav-link", href="/",
                                              children="Home")
                                   ]),
                                   html.Li(className="nav-item", children=[
                                       html.A(className="nav-link", href="/forum/post",
                                              children="Forum")
                                   ]),
                                   html.Li(className="nav-item", children=[
                                       dbc.DropdownMenu(nav=True, in_navbar=True, label="Blog",
                                                        children=[
                                                            dbc.DropdownMenuItem("View posts", href="/blog",
                                                                                 external_link=True),
                                                            dbc.DropdownMenuItem("Add post", href="/blog/add",
                                                                                 external_link=True),
                                                            dbc.DropdownMenuItem("About us", href="/about",
                                                                                 external_link=True),
                                                        ]),
                                   ]),

                                   html.Li(className="nav-item", children=[
                                       html.A(className="nav-link", id="third_nav")
                                   ]),
                                   html.Li(className="nav-item", children=[
                                       html.A(className="nav-link", id="forth_nav")
                                   ]),
                               ]),
                               search_button
                           ])

    full_navbar = dbc.Navbar(className="navbar", expand='lg', light=True, color='light',
                             children=[html.Div(className="container-fluid", children=[
                                 html.Img(
                                     src='data:image/png;base64,{}'.format(logo().decode()),
                                     width=50,
                                     style={'margin-right': 10, 'margin-left': -19},
                                     className='img-thumbnail'),
                                 html.A(dbc.NavbarBrand("Travelling Pants", href="/",
                                                        external_link=True)),
                                 dbc.NavbarToggler(id="navbar-toggler"),
                                 dbc.Collapse(id="navbar-collapse", navbar=True,
                                              children=[nav_buttons]),
                             ]),
                                       ])
    return full_navbar


def navigation_layout():
    page = dbc.Container(fluid=True, children=[
        # First row
        dbc.Row([
            # First column
            dbc.Col(width=4, children=[
                html.H2('TfL Zone 1 Navigation'),
                html.P(id="indicator"),
                html.P("Fill in your journey information below to check the route crowdedness"),
                dbc.Card(children=[
                    dbc.Container(
                        fluid=True, children=[
                            dbc.FormGroup([
                                html.Br(),
                                dbc.Toast(
                                    [dbc.Button(
                                        [html.I(className="fas fa-bus mr-2"), "BUS"]
                                        , id="bus_select", color="success",
                                        outline=False, n_clicks=0,
                                        active=True, style={'margin-right': 10}),
                                        dbc.Button(
                                            [html.I(className="fas fa-subway mr-2"), "TUBE"]
                                            , id="tube_select", color="success",
                                            outline=True, n_clicks=0)],
                                    header="Transportation mode:",
                                ),

                                dbc.Toast(
                                    [dcc.Dropdown(id='start_select',
                                                  placeholder='Search area',
                                                  value=None)],
                                    header="Start area:",
                                    icon="primary", ),

                                dbc.Toast(
                                    [dcc.Dropdown(id='end_select',
                                                  placeholder='Search area',
                                                  value=None)],
                                    header="Destination:",
                                    icon="danger", ),

                                html.Div(children=[
                                    dbc.Button("Clear", id="clear_button", type='reset',
                                               color="primary", className="mr-2",
                                               n_clicks=0),
                                    dbc.Button("Go", id="go_button",
                                               color="primary", className="mr-2",
                                               href='/analysis_dash/', external_link='True',
                                               n_clicks=0),
                                ])
                            ])
                        ])
                ])
            ]),

            # Second column
            dbc.Col(width=8, children=[dbc.Card(children=[
                dbc.Container(fluid=True, style={'display': 'inline-block', 'width': '100%'}, children=[
                    html.Br(),
                    html.H4("Important Information:"),
                    html.P("There will be a disruption in Tower Hill area for both Tube and Bus services")
                ]),
            ]),
                dcc.Store(id="path_memory", storage_type='session'),
                dcc.Store(id="mean_memory", storage_type='session'),
                dbc.Card(children=[
                    dbc.Container(fluid=True, style={'display': 'inline-block', 'width': '100%'},
                                  id="line_figure")
                ]),
            ]),
        ])

    ])
    return page


def analysis_layout():
    page = dbc.Container(fluid=True, style={'margin-bottom': 10},
                         children=[
                             html.H2('TfL Zone 1 Analysis'),
                             html.P(id="indicator"),
                             dbc.Card([
                                 dbc.Container(id='first_card')
                             ]),
                             dbc.Card([dcc.Store(id="path_memory", storage_type='session'),
                                       dcc.Store(id="mean_memory", storage_type='session'),
                                       dcc.Store(id="dataframe_memory"),
                                       dbc.Container(id='second_card')
                                       ]),
                             dbc.Card([
                                 dbc.Container(id='third_card', style={'display': 'inline-block', 'margin-bottom': 40},
                                               children=[
                                                   html.Br(),
                                                   dbc.Button("New Navigation", id="save_journey", color='primary',
                                                              external_link=True),
                                                   html.Span(style={'margin-bottom': 40, "margin-left": 10,
                                                                    "vertical-align": "middle"},
                                                             children="This will also save your journey in your profile travel history"),
                                               ])
                             ]),
                         ])
    return page

