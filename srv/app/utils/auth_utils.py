from functools import wraps
import base64

from flask import Request
from flask_login import current_user

from sap import xssec
from werkzeug import exceptions

from config import Config
from app.models import BaseUser, BasicUser, XsuaaUser


def get_xsuaauser_from_request(config: Config, request: Request) -> XsuaaUser | None:
    """
    Extracts the Bearer token from the request's Authorization header,
    creates an xssec security context using the provided config credentials,
    and returns an `XsuaaUser` instance if successful.

    :param config: Config object containing XSUAA credentials
    :param request: Flask Request object
    :return: `XsuaaUser` instance if token and context are valid, otherwise None
    """
    header_auth = request.headers.get("authorization")

    if not header_auth or not header_auth.startswith("Bearer"):
        return None

    access_token = header_auth[7:]

    xssec_context = xssec.create_security_context(
        access_token, config.get("AUTH_XSUAA_CRED")
    )

    return XsuaaUser(xssec_context) if xssec_context else None


def get_basicuser_from_request(config: Config, request: Request) -> BasicUser | None:
    """
    Extracts the Basic Auth credentials from the request's Authorization header,
    and returns a `BasicUser` instance if the credentials are valid.

    :param config: Config object containing user credentials
    :param request: Flask Request object
    :return: `BasicUser` instance if credentials are valid, otherwise None
    """
    header_auth = request.headers.get("authorization")

    if not header_auth or not header_auth.startswith("Basic "):
        return None

    auth = header_auth[6:]

    try:
        decoded = base64.b64decode(auth).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return None

    if not username or not password:
        return None

    users = config.get("AUTH_USERS", {})
    user_config = users.get(username)

    if user_config and user_config.get("password") == password:
        return BasicUser(username, user_config)

    return None


def roles_required(roles):
    """
    Customer Authorization Decorator to check if the user has the required roles.

    :param roles: List of roles to check

    :return: Decorated function
    """

    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if the user has scope using the xssec library
            user: BaseUser = current_user
            if all(user.check_scope(role) for role in roles):
                return f(*args, **kwargs)
            else:
                raise exceptions.Forbidden(
                    description=f"You do not have one or all roles required - {roles}"
                )

        return wrapper

    return decorated_function
