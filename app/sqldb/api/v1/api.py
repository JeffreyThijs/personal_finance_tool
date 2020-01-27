from flask import Blueprint, request
from flask_restplus import Resource, Api
from app import ma, db
from app.sqldb.api.v1.schemas import TransactionSchema, UserRegistrationSchema, UserLoginSchema
from app.sqldb.models import Transaction, User, RevokedTokenModel
from app.sqldb.api.v1 import _api as api
from app.sqldb.api.v1 import bp
from app.sqldb.api.v1.transactions import get_current_user_transactions, get_current_user_monthly_transactions
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)

class Transactions(Resource):
    @jwt_required
    def get(self):
        transactions = get_current_user_transactions()
        ts = TransactionSchema(many=True)
        return ts.dump(transactions)

class MonthlyTransactions(Resource):
    @jwt_required
    def get(self, year : str, month : str):
        transactions = get_current_user_monthly_transactions(year=year, month=month)
        ts = TransactionSchema(many=True)
        return ts.dump(transactions)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        try:
            # deserialize
            urs = UserRegistrationSchema()
            user = urs.load(data)

            # add user to db
            db.session.add(user)
            db.session.commit()

            # create jwt tokens
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token 
            }

        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        try:
            # deserialize
            urs = UserLoginSchema()
            user = urs.load(data)

            # create jwt tokens
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token 
            }

        except:
            return {'message': 'wrong login info'}, 500
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            db.session.add(revoked_token)
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            db.session.add(revoked_token)
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(SecretResource, '/secret')
api.add_resource(Transactions, '/transactions')
api.add_resource(MonthlyTransactions, '/transactions/<string:year>/<string:month>')