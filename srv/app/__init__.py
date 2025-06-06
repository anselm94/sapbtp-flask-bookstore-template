import os

from flask import Flask
from flask_login import LoginManager

from sap.cf_logging import flask_logging
from dotenv import load_dotenv

from app.database import DatabaseManager
from config import Config, config_manager

# Load environment variables from .env file (development)
load_dotenv()

# Load extensions
login_manager = LoginManager()
db_manager = DatabaseManager()


def create_app():
    """
    Create and configure the Flask application.
    This function initializes the Flask application, sets up logging,
    config, authentication, and database management.
    """

    # create Flask app
    app = Flask(__name__)

    # initialize configuration
    config: Config = config_manager.get(os.getenv("FLASK_ENV") or "DEV")

    # setup logging if only in production - else logs become JSON formatted to read
    if config.ENV == "PRODUCTION":
        flask_logging.init(app, config.LOGGING_LEVEL)

    # load config
    app.config.from_object(config)

    # setup authentication
    login_manager.init_app(app)

    # setup database
    db_manager.init_app(app)

    # dynamic imports since `db_manager` is not yet initialized
    from . import routes

    app.add_url_rule(
        "/health",
        view_func=routes.health_check,
        methods=["GET"],
        endpoint="health_check",
    )

    # register routes via blueprint
    app.register_blueprint(routes.bp, url_prefix="/api/v1")

    return app
