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

    CONTENT_STYLE = {
        "margin-right": "2rem",
        "padding": "1rem 1rem",

    }
    layout = dbc.Container(
        [
            html.H1("Create New Run"),
            html.Hr(),
            setting_form,
            html.Div([
                dcc.Loading(
                    id="loading-2",
                    children=[dbc.Row(html.Div(id='container', children=[]), style=CONTENT_STYLE),
                              dbc.Button("Submit", id='submit-val', color="primary", className="mr-1", n_clicks=0,
                                         style={'display': 'none'}),
                              dbc.Row([
                                  dbc.Badge("Success", color="success", className="mr-1", pill=True),
                                  dcc.Link(
                                      dbc.Button("Show Results", id='show-results', color="primary",
                                             className="mr-1", n_clicks=0),
                                      href='/results')],
                                    id='show_result_row', style={'display': 'none'})
                              ],
                    type="dot",
                    fullscreen=True
                    )
                ]),
            html.Div(id='params_value', style={'display': 'none'}),
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


section_dict = {
    "Basic system params":[('annual_production_capacity','Annual Production Capacity'),
                           ('contract_tarrif_range', 'Contract Tariff'),
                           ('production_degredeation', 'Production Degradation'),
                            ('project_years', 'Project Duration'),
                            ('yeild', 'Yield'),
                           ('initial_investment', 'Initial Investment')],
    "Depreciation & Taxes":[
        ('Corporate_tax','Corporate Tax'),
        ('Depreciation_period', 'Depreciation Period'),
        ('Depreciation', 'Depreciation'),
        ('Corporate_Tax', 'Corporate Tax'),
        ('number_active_days_year_1', 'Number Active_Days Year_1'),
        ('total_number_days_year_1', 'Total Number Days Year 1'),
        ('number_active_days_last_year', 'Number Active Days Last Year'),
        ('total_number_days_last_year', 'Total Number Days Last Year'),
        ('substitute_tax', 'substitute tax'),
        ('percent_EBITDA_for_corp_tax', 'Percent EBITDA for Corporate Tax'),
        ('vat_substitute_tax', 'VAT substitute Tax'),
        ('recivable_sales_cycle', 'Receivable Sales Cycle [days]'),
        ('payable_sales_cycle', 'Payable Sales Cycle [days]')
    ],
    "Operational Expenses": [('inflation','Inflation'),
                             ('VAT', 'VAT'),
                             ('lease', 'Lease [Euro/kWp]'),
                             ('OandM' 'O&M [Euro/kWp]'),
                             ('insurance', 'Insurance [Euro/kWp]'),
                             ('inverter_reserve', 'Inverter Reserve [Euro/kWp]'),
                             ('asset_management', 'Asset Management [Euro/kWp]'),
                             ('bank_agency_fees_and_others', 'Bank Agency Fees and Others [Euro/kWp]]')
                             ],

    "Financing": [("equity_portion", 'Equity Portion'),
                  ('interest_rate_range', 'Interest Rate'),
                    ('VAT_loan_interest_rate', 'VAT Loan Interest Rate'),
                    ('VAT_loan_return_period','VAT Loan Return Period'),
                  # ('interest_diff', 'interest_diff')
                    ('cost_of_capital', 'Cost of Capital'),
                    ('is_DSRA_requires', 'Is DSRA Requires'),
                    ('DSRA_Year_Start', 'DSRA Year Start'),
                  ('DSRA_period', 'DSRA Period'),
                  ]
}


def create_param_row(param):
    print('here2')
    return [dbc.Row(
        [dbc.FormGroup([
            dbc.Label(f"{param[1]}"),
            dbc.Input(type="number", id=f"get-{param[0]}-row")]
        )]
    )]


def create_section_form(section):
    print('here1')
    return [dbc.Row(
        [dbc.FormGroup([
            dbc.Label(f"{param[1]}"),
            dbc.Input(type="number", id=f"get-{param[0]}-row")]
        )]
    ) for param in section_dict[section]]

# # [html.H5(f'{section}:')]
# create_params_form = 0
# dbc.Form(
#     [

create_params_form = dbc.Form([
    dbc.Col([
        html.H5('Financing'),
        dbc.Row([
            dbc.FormGroup([
                dbc.Label(f"Annual Production Capacity"),
                dbc.Input(type="number", id=f"get-annual-production-capacity-row")]
                )
            ]
        )
      ]
     )
  ]
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

            html.Hr()  # horizontal line

        ])
