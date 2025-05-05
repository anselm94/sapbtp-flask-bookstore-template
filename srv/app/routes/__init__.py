from flask import current_app, jsonify, Blueprint, Request

from flask_login import login_required

from werkzeug import exceptions

from app.utils.auth_utils import roles_required
from app import login_manager
from app.utils.auth_utils import get_xssec_security_context
from app.services import books_service
from app.models import User

bp = Blueprint("routes", __name__)

#################
### CALLBACKS ###
#################

@login_manager.request_loader
def load_user_from_request(request: Request):
    """
    Load the user from the request using the SAP `xssec` security context.
    """
    security_context = get_xssec_security_context(current_app.config, request)

    user = User(security_context) if security_context else None
    return user


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


##############
### ROUTES ###
##############


@bp.route("/books", methods=["GET"])
@login_required
@roles_required(["uaa.resource"])
def get_books():
    books = books_service.get_books()
    return jsonify(books)
