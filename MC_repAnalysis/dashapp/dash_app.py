import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from .apps import new_run, run_history, results
from .apps.new_run import parse_contents, create_params_form, crate_file_uploader


VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}


LOGO = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fin.linkedin.com%2Fcompany%2Fgreenenesysgroup&psig=AOvVaw0nKxnBBs2-HBf4EYdsNQvE&ust=1614404958930000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjSsLvthu8CFQAAAAAdAAAAABAD'

def init_app(server):
    dash_app = dash.Dash(__name__, suppress_callback_exceptions=True, \
                meta_tags=[{'name':'viewport', \
                                'content':'width=device-width, initial-scale=1.0'}], \
                                external_stylesheets=[dbc.themes.BOOTSTRAP])
    auth = dash_auth.BasicAuth(
        dash_app,
        VALID_USERNAME_PASSWORD_PAIRS
    )

    search_bar = dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
            dbc.Col(
                dbc.Button("Search", color="primary", className="ml-2"),
                width="auto",
            ),
        ],
        no_gutters=True,
        className="ml-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )

    ## Upper Nav bar

    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Invetment Analysis App", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://greenenesys.com",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
        ],
        color="dark",
        dark=True,
        sticky = 'top'
    )


    # the style arguments for the sidebar. We use position:fixed and a fixed width
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 60,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("New run", href="/new_run", active="exact"),
                    dbc.NavLink("Run History", href="/run_history", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    dash_app.layout = html.Div([dcc.Location(id="url"),navbar , sidebar, content ])

    init_callbacks(dash_app)
    return  dash_app.server


def init_callbacks(dash_app):
    
    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            return html.P("This is the content of the home page!")
        elif pathname == "/new_run":
            return new_run.new_run_layout(dash_app)
        elif pathname == "/run_history":
            return run_history.run_history_layout(dash_app)
        elif pathname == "/results":
            return results.results_layout(dash_app)
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
    
    ## Takes input from file uploader and call pareser to read data
    @dash_app.callback(Output('output-data-upload', 'children'),
                Input('upload-data', 'contents'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children


    ## dinamically add menues
    @dash_app.callback(
        Output('container', 'children'),
        [Input('get-input-row', 'value')],
        [State('container', 'children')])
    def add_input_collection(input_value, div_children):
        div_children = []
        new_child = html.Div([])
        if input_value == 'upload':
            new_child = html.Div([crate_file_uploader])
        elif input_value == 'form':
            new_child = html.Div([create_params_form])

        div_children.append(new_child)
        return div_children
