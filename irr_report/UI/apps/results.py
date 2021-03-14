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


layout = dbc.Container(
    [
        html.H1("Results page"),
        html.Hr()
    ],
    fluid=True
)