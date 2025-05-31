from typing import Optional
from datetime import date, datetime
from abc import ABC, abstractmethod

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    SmallInteger,
    Numeric,
    Date,
    UUID,
)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sap import xssec

from app import db_manager
from config import UserConfig


###################
### AUTH MODELS ###
###################


class BaseUser(ABC):
    """
    Abstract base class for user types.
    """

    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Checks if the user is authenticated
        """
        pass

    @abstractmethod
    def is_active(self) -> bool:
        """
        Checks if the user is active
        """
        pass

    @abstractmethod
    def is_anonymous(self) -> bool:
        """
        Checks if the user is a technical/system user or not
        """
        pass

    @abstractmethod
    def check_scope(self, scope: str) -> bool:
        """
        Checks if the user has the specified scope
        :param scope: The scope to check
        :return: True if the user has the scope, False otherwise
        """
        pass

    @abstractmethod
    def get_id(self) -> str:
        """
        Returns the unique identifier of the user
        :return: Unique identifier of the user
        """
        pass


class BasicUser(BaseUser):
    """
    User class representing the authenticated user in the application
    using Flask-Login to represent the current user session, once the
    user is authenticated via basic authentication.

    See `flask-login` docs: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, user_id: str, user_config: UserConfig):
        self.user_id = user_id
        self.user_config = user_config

    def is_authenticated(self) -> bool:
        return self.user_config is not None

    def is_active(self) -> bool:
        return self.user_config is not None

    def is_anonymous(self) -> bool:
        return self.user_config is None

    def check_scope(self, role: str) -> bool:
        return role in self.user_config.get("roles", [])

    def get_id(self) -> str:
        return self.user_id

    def __repr__(self):
        return f"<BasicUser user_id={self.user_id}, " f"user_config={self.user_config}>"


class XsuaaUser(BaseUser):
    """
    User class representing the authenticated user in the application
    using Flask-Login to represent the current user session.

    Uses SAP's `xssec` library to represent user's authentication & authorization
    context.

    See `flask-login` docs: https://flask-login.readthedocs.io/en/latest/#your-user-class
    """

    def __init__(self, xssec_security_context: xssec.SecurityContextXSUAA):
        self.security_context = xssec_security_context

    def is_authenticated(self) -> bool:
        return self.security_context is not None

    def is_active(self) -> bool:
        return self.security_context is not None

    def is_anonymous(self) -> bool:
        return self.email() is None

    def check_scope(self, scope: str) -> bool:
        return self.security_context.check_scope(scope)

    def get_id(self) -> str:
        return self.client_id()

    def subaccount_id(self) -> str:
        return self.security_context.get_subaccount_id()

    def client_id(self) -> str:
        return self.security_context.get_clientid()

    def email(self) -> Optional[str]:
        return self.security_context.get_email()

    def logon_name(self) -> str:
        return self.security_context.get_logon_name() or "Anonymous"

    def __repr__(self):
        return (
            f"<XsuaaUser client_id={self.client_id()}, "
            f"subaccount_id={self.subaccount_id()}, "
            f"email={self.email()}, "
            f"logon_name={self.logon_name()}, "
            f"security_context={self.security_context}>"
        )


#################
### DB MODELS ###
#################

######################## IMPORTANT NOTE #########################################
# The models are defined in `db/schema.cds`. The `@sap/cds-dk` tooling takes
# care of generating HANA HDI artefacts for creating & managing tables & other
# entities. You can view the generated artefacts in the `gen/db/src/gen` folder
# for reference while modeling the below classes.
#
# The classes below are merely an object-relational mapping (ORM) representation
# of the corresponding database tables. You must keep the models in sync with the
# CDS definitions in `db/schema.cds` file.
##################################################################################

BOOKSTORE_NAMESPACE = "SAP_SAMPLE_BOOKSHOP"
COMMON_NAMESPACE = "SAP_COMMON"

# alias
Model = db_manager.db.Model


class Books(Model):
    __tablename__ = f"{BOOKSTORE_NAMESPACE}_BOOKS"

    ID: Mapped[int] = mapped_column(primary_key=True)

    createdBy: Mapped[str] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    modifiedBy: Mapped[str] = mapped_column(String(255))
    modifiedAt: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    title: Mapped[str] = mapped_column(String(111), nullable=False)
    descr: Mapped[str] = mapped_column(String(1111))
    stock: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(9, 2))

    AUTHOR_ID: Mapped[int] = mapped_column(
        ForeignKey(f"{BOOKSTORE_NAMESPACE}_AUTHORS.ID")
    )
    author: Mapped["Authors"] = relationship(back_populates="books")

    genre_ID: Mapped[int] = mapped_column(
        ForeignKey(f"{BOOKSTORE_NAMESPACE}_GENRES.ID")
    )
    genre: Mapped["Genres"] = relationship()

    currency_code: Mapped[str] = mapped_column(
        String(3), ForeignKey(f"{COMMON_NAMESPACE}_CURRENCIES.code")
    )
    currency: Mapped["Currencies"] = relationship()


class Authors(Model):
    __tablename__ = f"{BOOKSTORE_NAMESPACE}_AUTHORS"

    ID: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(111), nullable=False)
    dateOfBirth: Mapped[Optional[date]] = mapped_column(Date)
    dateOfDeath: Mapped[Optional[date]] = mapped_column(Date)
    placeOfBirth: Mapped[Optional[str]] = mapped_column(String)
    placeOfDeath: Mapped[Optional[str]] = mapped_column(String)

    books: Mapped[list["Books"]] = relationship(back_populates="author")


class Genres(Model):
    __tablename__ = f"{BOOKSTORE_NAMESPACE}_GENRES"

    ID: Mapped[str] = mapped_column(UUID, primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descr: Mapped[Optional[str]] = mapped_column(String(1000))

    parent_ID: Mapped[str] = mapped_column(
        ForeignKey(f"{BOOKSTORE_NAMESPACE}_GENRES.ID")
    )
    parent: Mapped["Genres"] = relationship(remote_side=[ID])
    children: Mapped[list["Genres"]] = relationship(back_populates="parent")


class Currencies(Model):
    __tablename__ = f"{COMMON_NAMESPACE}_CURRENCIES"

    code: Mapped[str] = mapped_column(String(3), primary_key=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    descr: Mapped[Optional[str]] = mapped_column(String(1000))
    symbol: Mapped[Optional[str]] = mapped_column(String(5))
    minorUnit: Mapped[Optional[int]] = mapped_column(SmallInteger())
