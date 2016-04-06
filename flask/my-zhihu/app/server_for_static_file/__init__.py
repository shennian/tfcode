from flask import Blueprint

static_file = Blueprint('static_file', __name__)

from . import views