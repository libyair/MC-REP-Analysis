import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from .apps import new_run, run_history, results
from .apps.new_run import parse_contents, create_params_form, crate_file_uploader
from .apps.results import load_annual_table, display_metrics, display_cash_flow, display_params
from .apps.run_history import split_filter_part
import json
import subprocess as sub
from .apps.data_handler import *
from flask import request, session
import os

from dash_extensions.snippets import send_data_frame

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
        "width": "12rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "14rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Run History", href="/run_history", active="exact"),
                    dbc.NavLink("New run", href="/new_run", active="exact")
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    dash_app.layout = html.Div([
        dcc.Store(id='results-store-submit', storage_type='session'),
        dcc.Store(id='results-store-history', storage_type='session'),
        dcc.Store(id='excel-store', storage_type='session'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content])

    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    
    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/":
            # return run_history.run_history_layout(dash_app)
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
    @dash_app.callback([Output('params_value', 'params'),
                       Output('output-data-upload', 'children'),
                        Output('submit-val', 'style')],
                       Input('upload-data', 'contents'),
                        State('upload-data', 'filename'),
                        State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                json_params, data_table = parse_contents(c, n, d)

            children = [data_table]
            if json_params:
                return json.dumps(json_params, default=convert), children, {}
            else:
                return '', children, {'display': 'none'}
        else:
            return '', '', {'display': 'none'}
            
    # dynamically add menus
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


    @dash_app.callback(
         [Output('results-store-submit', 'data'), #Output('session-data', 'children'),
          Output('show_result_row', 'style')],
        [Input('params_value', 'params'),
        Input('run-name-row', 'value'),
        Input('submit-val', 'n_clicks')])
    def submit_run(params, value, n_clicks): #result_data
        if n_clicks > 0:

            # create json:
            run_data = {
               'name': value,
               'params': params,
               'creator': request.authorization['username']
            }

            id = update_db(run_data)
            # Activate script using id
            cwd = os.getcwd()
            try:
                # Run the process
                print( f"{cwd}\MC_repAnalysis\irr_report\irr_report.py")
                sub.check_output(["irr_report_env/Scripts/python",
                      f"{cwd}\MC_repAnalysis\irr_report\irr_report.py",
                      f"--id", str(id)
                      ])
                # load data from db to store
                result_data = get_run_results(id)
                print('result_data: ', result_data)
                return result_data[0], {}

            except sub.CalledProcessError as e:
                print(e.output)
                return {}, {'display': 'none'}
        return {}, {'display': 'none'}

    # Callback to handle results accordion structure
    card_names = ['params', 'metrics', 'cash-flow-components', 'tables']
    toggle_input = [Input(f"group-{nameID}-toggle", "n_clicks") for nameID in card_names]
    toggle_input.extend([
        Input('results-store-submit', 'data'),
        Input('results-store-submit', 'modified_timestamp'),
        Input('results-store-history', 'data'),
        Input('results-store-history', 'modified_timestamp')
    ])

    toggle_output = [Output(f"collapse-{nameID}", "is_open") for nameID in card_names]
    toggle_output.extend([Output(f"{nameID}-div", "children") for nameID in card_names])
    toggle_output.extend([Output("excel-store", "data"), Output('export-button', 'style')])

    toggle_state = [State(f"collapse-{nameID}", "is_open") for nameID in card_names]
    toggle_state.extend([State(f"{nameID}-div", "children") for nameID in card_names])

    @dash_app.callback(
        toggle_output,
        toggle_input,
        toggle_state
    )
    def toggle_accordion(n1, n2, n3, n4, run_results_submit, t_submit, run_results_history, t_history,
                         is_open1, is_open2, is_open3, is_open4, s1, s2, s3, s4):
        ctx = dash.callback_context
        data = None
        results_dict = None
        excel_dic = {}
        btn_style = {'display': 'none'}
        if t_submit and t_history:
            if t_submit < t_history:
                data = run_results_history
            else:
                data = run_results_submit
        elif t_submit:
            data = run_results_submit
        elif t_history:
            data = run_results_history

        if data:
            results_dict = json.loads(data['results'])
            params_dict = json.loads(data['params'])
            mc = data['MC']

        if not ctx.triggered:
            return False, False, False, False, s1, s2, s3, s4, excel_dic, btn_style
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "group-params-toggle" and n1:
            if is_open1:
                return not is_open1, is_open2, is_open3, is_open4, s1, s2, s3, s4, excel_dic, btn_style
            else:
                if results_dict:
                    params_div = display_params(mc, params_dict, data['name'],
                                                data['date'], data['creator'],
                                                data['status'])
                else:
                    params_div = [html.P("No data to show")]
                return not is_open1, is_open2, is_open3, is_open4, params_div, s2, s3, s4, excel_dic, btn_style
        elif button_id == "group-metrics-toggle" and n2:
            if is_open2:
                return is_open1, not is_open2, is_open3, is_open4, s1, s2, s3, s4, excel_dic, btn_style
            else:
                if results_dict:
                    metrics_div = display_metrics(mc, results_dict)
                else:
                    metrics_div = [html.P("No data to show")]
                return is_open1, not is_open2, is_open3, is_open4, s1, metrics_div, s3, s4, excel_dic, btn_style

        elif button_id == "group-cash-flow-components-toggle" and n3:
            if is_open3:
                return is_open1, is_open2, not is_open3, is_open4, s1, s2, s3, s4, excel_dic, btn_style
            else:
                if results_dict:
                    div_cash_flow = display_cash_flow(mc, results_dict)
                else:
                    div_cash_flow = [html.P("No data to show")]
                return is_open1, is_open2, not is_open3, is_open4, s1, s2, div_cash_flow, s4, excel_dic, btn_style

        elif button_id == "group-tables-toggle" and n4:
            if is_open4:
                return is_open1, is_open2, is_open3, not is_open4, s1, s2, s3, s4, excel_dic, btn_style
            else:
                if results_dict:
                    annual_table_div = load_annual_table(results_dict['annual_results'], mc)
                    excel_dic = {'data': results_dict['annual_results'],
                                  'name':  data['name']}
                    btn_style = {}
                else:
                    annual_table_div = [html.P("No data to show")]
                return is_open1, is_open2, is_open3, not is_open4, s1, s2, s3, annual_table_div,\
                            excel_dic, btn_style

        return False, False, False, False, s1, s2, s3, s4, excel_dic, btn_style




    @dash_app.callback(
        Output('run-history-table', 'data'),
        Input('run-history-table', "page_current"),
        Input('run-history-table', "page_size"),
        Input('run-history-table', 'sort_by'),
        Input('run-history-table', 'filter_query'))
    def update_table(page_current, page_size, sort_by, filter):
        filtering_expressions = filter.split(' && ')
        user_name = request.authorization['username']
        df = get_run_history_data(user_name)

        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        page = page_current
        size = page_size
        return dff.iloc[page * size: (page + 1) * size].to_dict('records')

    # Show run button in run history
    @dash_app.callback(
        [Output('results-store-history', 'data'),
         Output('show-run-history-result-row', 'style')],
        [Input('run-history-table', 'active_cell')],
        State('run-history-table', 'data'))
    def show_run_history_results(active_cell, data):  # result_data
        if active_cell:
            row = active_cell['row']
            rowData = data[row]
            print('cellData:', rowData)
            id_ = rowData['id']
            result_data = get_run_results(id_)
            print('type: ', type(result_data[0]))
            return result_data[0], {}

        return {}, {'display': 'none'}

    @dash_app.callback(Output("download", "data"),
                       [Input("export-btn", "n_clicks"),
                        Input("excel-store", "data")])
    def generate_xlsx(n_clicks, excel_data):
        if n_clicks:
            df = pd.DataFrame(excel_data['data'])
            return send_data_frame(df.to_csv, filename=f"{excel_data['name']}_annual_results.csv")

        return



