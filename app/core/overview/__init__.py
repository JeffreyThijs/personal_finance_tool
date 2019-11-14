from flask import Blueprint

bp = Blueprint('overview', __name__)

from app.core.overview import routes