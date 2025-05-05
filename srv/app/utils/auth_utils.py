from functools import wraps

from flask import Request
from flask_login import current_user

from sap import xssec
from werkzeug import exceptions

from config import Config
from app.models import User


def get_xssec_security_context(config: Config, request: Request):
    """
    Creates the `xssec` security context from the request's `Authorization` header
    """
    header_auth = request.headers.get("authorization")

    if not header_auth or not header_auth.startswith("Bearer"):
        return None

    access_token = header_auth[7:]

    return xssec.create_security_context(access_token, config.get("CFCRED_XSUAA"))


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
            user: User = current_user
            if all(user.check_scope(role) for role in roles):
                return f(*args, **kwargs)
            else:
                raise exceptions.Forbidden(
                    description=f"You do not have one or all roles required - {roles}"
                )

        return wrapper

    return decorated_function
