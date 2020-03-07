from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('api', __name__)
_api = Api(bp)

from app.sqldb.api.v1 import api