import logging

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase

log = logging.getLogger("database-manager")


class Base(DeclarativeBase):
    pass


class DatabaseManager:
    """
    SQLAlchemy Flask extension manager

    Manages the reference to the `db` instance and initializes the bootstrapping
    of the database connection
    """

    def __init__(self, model_class=Base):
        self.model_class = model_class
        self.db = SQLAlchemy(model_class=self.model_class)

    def init_app(self, app):
        log.info(
            f"Initializing database manager via SQLAlchemy using URL - {app.config.get('SQLALCHEMY_DATABASE_URI')}..."
        )
        self.db.init_app(app)
