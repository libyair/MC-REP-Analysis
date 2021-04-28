import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import datetime
# from app import app
# from app import server
import io
import base64
import pandas as pd
import dash_table
import flask
import numpy as np
from dash_extensions import Download
import plotly.express as px

def results_layout(dash_app):

    accordion = html.Div(
        [make_item('params', 'Run parameters'), make_item('metrics', 'Metrics'), make_item('cash-flow-components', 'Cash Flow Components'),
         make_item('tables', 'Data Tables')],
        className="accordion"
    )


    layout = dbc.Container(
        html.Div(
        [
            html.H1("Results page"),
            html.Hr(),
            accordion
        ]),
    )

    return layout


def make_item(nameID, presrnted_name):
    # we use this function to make the example items to avoid code duplication
    print(f"group-{nameID}-toggle")
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        presrnted_name,
                        color="link",
                        id=f"group-{nameID}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    [html.Div(id=f"{nameID}-div", children=[]),
                     html.Div(id='export-button',
                       children=[html.Button("Export", id="export-btn"), Download(id="download")],
                             style={'display': 'none'})
                        ]
                    ),
                id=f"collapse-{nameID}",
            ),
        ]
    )


def display_params(mc, params_dict, name, date, creator, status):
    df_params = pd.DataFrame.from_dict(params_dict, orient='index',
                                       columns=['Value']
                                       )
    df_params['Parameter'] = list(params_dict.keys())
    print(df_params)

    table1 = dbc.Table.from_dataframe(df_params[['Parameter', 'Value']].iloc[0:17],
                                                bordered=True, hover=True)
    table2 = dbc.Table.from_dataframe(df_params[['Parameter', 'Value']].iloc[18:-1],
                                      bordered=True, hover=True)

    return [
        html.H4(f"Run Name: {name}"),
        html.H4(f"Execution time: {date}"),
        html.H4(f"Creator: {creator}"),
        html.H4(f"Status: {status}"),
        dbc.Row([
            dbc.Col(table1, width='auto', lg=6),
            dbc.Col(table2, width='auto', lg=6),
            ])
    ]



def display_metrics(mc, results_dict):
    if not mc:
        irr_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(f"{round(results_dict['mean_IRR']*100,2)}", className="card-title"),
                    html.H6("IRR [%]", className="card-subtitle")]))

        npv_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(f"{round(results_dict['mean_NPV']):,}", className="card-title"),
                    html.H6("NPV [$]", className="card-subtitle")]))

        prob_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(f"{round(results_dict['mean_payback'],2)}", className="card-title"),
                    html.H6("Payback period [Years]", className="card-subtitle")]))

        return [dbc.Row(
                        [dbc.Col(irr_card, width="auto"),
                         dbc.Col(npv_card, width="auto"),
                         dbc.Col(prob_card, width="auto")])]
    else:
        return []


def load_annual_table(annual_dict, mc):
    if not mc:
        annual_df = pd.DataFrame(annual_dict)
        annual_df = annual_df.round(2)
        annual_df.insert(0, 'Year', np.arange(1, len(annual_df)+1))
        table = dash_table.DataTable(
            id='annual-results-table',
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in annual_df.columns
            ],
            data=annual_df.to_dict('records'),
            style_table={'overflowY': 'auto', 'overflowx': 'auto'}
        )

        return [table]

    else:
        return []


def display_cash_flow(mc, data_dict):

    if not mc:
        annual_df = pd.DataFrame(data_dict['annual_results'])
        annual_df.insert(0, 'Years', np.arange(1, len(annual_df)+1))

        return [dbc.Row(
                    [dbc.Col(_add_plot(name, annual_df[['Years', name]]),
                            width='auto', lg=6) for name in ['OPEX', 'Annual_revenue',
                                                       ]]
                ),
            dbc.Row(
                [dbc.Col(_add_plot(name, annual_df[['Years', name]]),
                         width='auto', lg=6) for name in [
                                                          'Cash Flow Available for Dividends',
                                                          'Delta_working_capital']]
            ),
                dbc.Row(
                    [dbc.Col(_add_plot(name, annual_df[['Years', name]]),
                            width='auto', lg=6) for name in ['Annual_loan_return',
                                                       'Annual_corp_tax'
                                                       ]]
                ),
            dbc.Row(
                [dbc.Col(_add_plot(name, annual_df[['Years', name]]),
                         width='auto', lg=6) for name in [
                                                          'Annual_interes_return',
                                                          'UpfrontFee_and_Substitute_TaxCapex']]
            )
            ]

    else:
        return []


def _add_plot(name, df):
    fig = px.line(df, x='Years', y=name)
    return dcc.Graph(figure=fig)

