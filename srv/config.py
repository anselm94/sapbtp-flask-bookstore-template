import os, logging

from cfenv import AppEnv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize cfenv to get environment variables
cfenv = AppEnv()


class Config(object):
    # Runtime
    ENV = "DEV"

    # Server configuration
    HOST = os.environ.get("HOST")
    PORT = int(os.environ.get("PORT"))

    # Logging
    LOGGING_LEVEL: int = os.environ.get("LOGGING_LEVEL", logging.INFO)

    # Cloud Foundry - Credentials
    CFCRED_XSUAA: dict = cfenv.get_service(label="xsuaa").credentials
    CFCRED_HANA: dict = cfenv.get_service(label="hana").credentials

    ## Database - HANA
    DB_TYPE: str = "hana"
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


class DevelopmentConfig(Config):
    ENV = "DEV"

    # Server configuration
    HOST = "localhost"
    PORT = 5000


class TestConfig(Config):
    ENV = "TEST"


class ProductionConfig(Config):
    ENV = "PRODUCTION"

    # Server configuration
    HOST = "0.0.0.0"  # Bind to all interfaces
    PORT = int(
        os.environ.get("PORT", 8080)
    )  # 8080 is the default port for Cloud Foundry


config_manager = {
    "DEV": DevelopmentConfig,
    "TEST": TestConfig,
    "PRODUCTION": ProductionConfig,
}
