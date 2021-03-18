from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .dashapp.dash_app import init_app
        app = init_app(app)

        return app