import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from app import server

from apps import new_run, run_history, results

# LOGO = r"C:\Users\talz\OneDrive\Documents\Yair\greenennesis\MC-REP-Analysis\irr_report\resources\logo.png"





if __name__ == '__main__':
    app.run_server(debug=True)