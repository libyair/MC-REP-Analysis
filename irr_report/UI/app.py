import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}




app = dash.Dash(__name__, suppress_callback_exceptions=True, \
                meta_tags=[{'name':'viewport', \
                                'content':'width=device-width, initial-scale=1.0'}], \
                                external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


server = app.server



# if __name__ == '__main__':
#     app.run_server(debug=True)