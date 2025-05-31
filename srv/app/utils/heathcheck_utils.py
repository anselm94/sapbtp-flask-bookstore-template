from typing import TypedDict, Dict, Literal

from sqlalchemy import text

from app import db_manager
from config import Config

db = db_manager.db


class ComponentHealthCheckStatus(TypedDict):
    """
    Represents the health check status of a component.
    """

    status: Literal["UP", "DOWN"]


class HealthCheckStatus(ComponentHealthCheckStatus):
    """
    Represents the overall health check status of the application,
    including the status of its components.
    """

    components: Dict[str, ComponentHealthCheckStatus]


def run_health_check(config: Config) -> HealthCheckStatus:
    """
    Run the health check for the application.

    Checks the status of various components of the application,
    such as the database, and returns their health status.
    """
    return HealthCheckStatus(
        status="UP",
        components={
            "db": run_health_check_db(config),
        },
    )


##############
# COMPONENTS #
##############
def run_health_check_db(config: Config) -> ComponentHealthCheckStatus:
    """
    Run the health check for the database component
    """
    # use SQLite/HANA specific query to check database connectivity
    statement = "SELECT 1 FROM DUMMY" if config.get("DB_TYPE") == "hana" else "SELECT 1"

    return ComponentHealthCheckStatus(
        status=("UP" if db.session.execute(text(statement)).scalar() else "DOWN"),
    )
