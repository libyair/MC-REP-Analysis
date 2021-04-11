import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
import io
import base64
import pandas as pd
import dash_table
import flask
import os
from .data_handler import get_params
import json

def new_run_layout(dash_app):
    run_name_input = dbc.FormGroup(
        [
            dbc.Label("Run Name:", html_for="run-name-row", width=4),
            dbc.Col(
                dbc.Input(
                    type="run_name", id="run-name-row", placeholder="Enter run name"
                ),
                width=10,  align="center"
            ),

        ],
        row=True
    )

    data_insertion_method_input = dbc.FormGroup(
        [
            dbc.Label("Get input:", html_for="data_insertion_method-row", width=6 ),
            dbc.Col(
                dbc.RadioItems(
                    id="get-input-row",
                    options=[
                        {"label": "Upload file", "value": 'upload'},
                        {"label": "Fill form", "value": 'form'},
                    ],
                ),
                width=12,  align="center"
            )
        ],
        row=True
    )

    setting_form = dbc.FormGroup( [
        dbc.Row(
            [run_name_input], 
            align="center"
        ),
        dbc.Row([data_insertion_method_input], 
            align="center"
        ) 
    ] )

    layout = dbc.Container(
        [
            html.H1("Create New Run"),
            html.Hr(),
            setting_form,
            html.Div(id='container', children = []),
            html.Div(id='params_value', style={'display': 'none'}),
            html.Div(id='submit_button_container', style={'display': 'none'})
        ],
        fluid=True
    )

    return layout

crate_file_uploader = html.Div([ 
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
            ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
        ),
    html.Div(id='output-data-upload')
    ])

create_params_form = dbc.FormGroup(
    [
        dbc.Label("Get data:", html_for="get-data-row", width=4),
        dbc.Col(
            dbc.Input(
                type="get_data", id="get-data-row", placeholder="Enter number"
            ),
            width=10,  align="center"
        ),

    ],
    row=True
)

    
## Handleing getting a file
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise ValueError
    except Exception as e:
        print(e)
        return None, html.Div([
            'Unsupported file format.'
        ])
    else:
        json_params, missing_params = get_params(df)
        print(missing_params)
        if len(missing_params) > 0:
            #Found missing param - return error
            erorString = 'The following params are missing: \n '
            for param in missing_params:
                erorString = erorString + param + '\n'
            return None, html.Div([erorString])
        return json_params, html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_table={'overflowX': 'scroll'}
            ),

            html.Hr(),  # horizontal line
            dbc.Button("Submit", id='submit-val', color="primary", className="mr-1", n_clicks=0)
            # dcc.Link(
            #     dbc.Button("Submit", id='submit-val', color="primary", className="mr-1",  n_clicks=0),
            #     href='/results')

        ])
