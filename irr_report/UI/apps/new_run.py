import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
from app import app
from app import server
import io
import base64
import pandas as pd
import dash_table
import flask


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

setting_form = dbc.Form( [
    dbc.Row(
        [run_name_input], 
        align="center"
    ),
    dbc.Row([data_insertion_method_input], 
        align="center"
    ) 
 ] )

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

create_params_form= dbc.FormGroup(
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

## dinamically add menues
@app.callback(
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
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns], 
            style_table={'overflowX': 'scroll'}
        ),

        html.Hr(),  # horizontal line
        dcc.Link(
            dbc.Button("Submit", id='submit-val', color="primary", className="mr-1"),
            href='/results')

    ])
## Takes input from file uploader and call pareser to read data
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



layout = dbc.Container(
    [
        html.H1("Create New Run"),
        html.Hr(),
        setting_form,
        html.Div(id='container', children = [])        
    ],
    fluid=True
)

