from flask import Blueprint

bp = Blueprint('prognosis', __name__)

from app.core.prognosis import routes