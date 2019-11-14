from flask import Blueprint

bp = Blueprint('home', __name__)

from app.core.home import routes