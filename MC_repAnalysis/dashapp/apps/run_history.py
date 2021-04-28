import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import request
# from dash_app import app
# from app import server
from .data_handler import get_run_history_data
import dash_table

def run_history_layout(dash_app):

    user_name = request.authorization['username']
    df = get_run_history_data(user_name)

    PAGE_SIZE = 20

    CONTENT_STYLE = {
        "margin-right": "2rem",
        "padding": "1rem 1rem",

    }
    layout = [html.H1(f"Hellp {user_name}"),
              html.Hr(),  # horizontal line
              html.H3(f"Run History"),
              dbc.Row(
                        [dcc.Link(
                            dbc.Button("Show run results", id='show-run-results', color="primary",
                                        className="mr-1", n_clicks=0),
                            href='/results')],
                  id='show-run-history-result-row', style={'display': 'none'}, justify="end"),
              dbc.Row(html.Div(id='container2', children=[]), style=CONTENT_STYLE),
              dash_table.DataTable(
                  id='run-history-table',
                  columns=[
                      {'name': i, 'id': i, 'deletable': True} for i in df.columns
                  ],
                  page_current=0,
                  page_size=PAGE_SIZE,
                  page_action='custom',
                  filter_action='custom',
                  filter_query='',
                  sort_action='custom',
                  sort_mode='multi',
                  sort_by=[],
                  fixed_rows={'headers': True},
                  style_table={
                      'maxHeight': '50ex',
                      'overflowY': 'scroll',
                      'width': '100%',
                      'minWidth': '100%',
                  },
                  style_cell={
                      'fontFamily': '-apple-system',
                      'textAlign': 'center',
                      'height': '60px',
                      'padding': '2px 22px',
                      'whiteSpace': 'inherit',
                      'overflow': 'hidden',
                      'textOverflow': 'ellipsis',
                  },
                  style_header={
                      'fontWeight': 'bold',
                      'backgroundColor': '#6c757d',
                  }

              )

        ]

    # TODO: 1. Add projects
    #       2. Add irr and mpv results as column to table
    return layout



operators = [['ge ', '>='],
                 ['le ', '<='],
                 ['lt ', '<'],
                 ['gt ', '>'],
                 ['ne ', '!='],
                 ['eq ', '='],
                 ['contains '],
                 ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3