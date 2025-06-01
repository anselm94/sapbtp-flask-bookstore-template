import os, logging
from typing import Literal, Dict, TypedDict

from cfenv import AppEnv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize cfenv to get environment variables
cfenv = AppEnv()


class UserConfig(TypedDict):
    """
    Configuration for a user in the application.
    """
    password: str
    roles: list[str]
    attr: dict


class Config(dict):
    # Runtime
    ENV = "DEV"

    # Server configuration
    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))

    # Logging
    LOGGING_LEVEL: int = os.environ.get("LOGGING_LEVEL", logging.INFO)

    # Authentication
    AUTH_TYPE: Literal["xsuaa", "basic"] = "basic"
    AUTH_USERS: Dict[str, UserConfig] = {
        "me": {
            "password": "me",
            "roles": ["uaa.resource"],
            "attr": {},
        }
    }

    ## Database - SQLite
    DB_TYPE: Literal["sqlite", "hana"] = "sqlite"
    DB_FILE: str = os.path.abspath("db.sqlite3")

    ## SQLAlchemy - Database URI
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}:///{DB_FILE}"


class DevelopmentConfig(Config):
    ENV = "DEV"

    # Server configuration
    HOST = "localhost"
    PORT = 5000


class ProductionConfig(Config):
    ENV = "PRODUCTION"

    # Server configuration
    HOST = "0.0.0.0"  # Bind to all interfaces
    PORT = int(
        os.environ.get("PORT", 8080)
    )  # 8080 is the default port for Cloud Foundry

    # Cloud Foundry - Credentials
    CFCRED_XSUAA: dict = cfenv.get_service(label="xsuaa").credentials
    CFCRED_HANA: dict = cfenv.get_service(label="hana").credentials

    # Authentication
    AUTH_TYPE: Literal["xsuaa", "basic"] = "xsuaa"
    AUTH_XSUAA_CRED: dict = CFCRED_XSUAA

    ## Database - HANA
    DB_TYPE: Literal["sqlite", "hana"] = "hana"
    DB_HOST: str = CFCRED_HANA["host"]
    DB_PORT: str = CFCRED_HANA["port"]
    DB_USER: str = CFCRED_HANA["user"]
    DB_PASSWORD: str = CFCRED_HANA["password"]
    DB_SCHEMA: str = CFCRED_HANA["schema"]

    ## SQLAlchemy - Database URI
    SQLALCHEMY_DATABASE_URI = (
        f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
        f"?encrypt=true&currentSchema={DB_SCHEMA}"
    )


config_manager = {
    "DEV": DevelopmentConfig,
    "PRODUCTION": ProductionConfig,
}
