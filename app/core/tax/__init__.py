from flask import Blueprint

bp = Blueprint('tax', __name__)

from app.core.tax import routes