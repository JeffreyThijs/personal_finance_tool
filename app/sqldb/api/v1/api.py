from flask import Blueprint
from flask_restplus import Resource, Api
from app import ma, db
from app.sqldb.api.v1.schemas import TransactionSchema
from app.sqldb.models import Transaction
from app.sqldb.api.v1 import _api as api
from app.sqldb.api.v1 import bp

@api.route('/transactions')
class Transactions(Resource):
    def get(self):
        t = TransactionSchema()
        return t.dump(db.session.query(Transaction).first())

# api.add_resource(HelloWorld, '/hello', '/world')