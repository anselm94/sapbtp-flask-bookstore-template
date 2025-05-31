from flask import current_app, jsonify, Blueprint, Request
from flask_login import login_required
from werkzeug import exceptions

from app import login_manager
from app.utils.auth_utils import (
    get_basicuser_from_request,
    get_xsuaauser_from_request,
    roles_required,
)
from app.services import books_service
from app.utils.heathcheck_utils import run_health_check
from app.models import BaseUser

#################
### CALLBACKS ###
#################


@login_manager.request_loader
def load_user_from_request(request: Request) -> BaseUser:
    """
    Load the user from the request using the configured authentication type.
    """
    if current_app.config.get("AUTH_TYPE") == "basic":
        return get_basicuser_from_request(current_app.config, request)
    elif current_app.config.get("AUTH_TYPE") == "xsuaa":
        return get_xsuaauser_from_request(current_app.config, request)
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    """
    Customize unauthorized 401 response for REST API
    """
    return {
        "error": {
            "code": 4010001,
            "message": "Unauthorized access",
        }
    }, 401


#######################
### ROUTES - COMMON ###
#######################


def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return (
        jsonify(run_health_check(current_app.config)),
        200,
    )


####################
### ROUTES - BP1 ###
####################

bp = Blueprint("routes", __name__)


@bp.errorhandler(exceptions.Forbidden)
def handle_forbidden(e: exceptions.Forbidden):
    """
    Customize forbidden 403 response for REST API
    """
    return {
        "error": {
            "code": 4030001,
            "message": e.description,
        }
    }, 403


@bp.route("/books", methods=["GET"])
@login_required
@roles_required(["uaa.resource"])
def get_books():
    books = books_service.get_books()
    return jsonify(books)
