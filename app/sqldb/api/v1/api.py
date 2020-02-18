from flask import Blueprint, request
from flask_restplus import Resource, Api
from app import ma, db
from app.sqldb.api.v1.schemas import *
from app.sqldb.models import Transaction, User, RevokedTokenModel
from app.sqldb.api.v1 import _api as api
from app.sqldb.api.v1 import bp
from app.sqldb.api.v1.transactions import (get_current_user_transactions, 
                                           get_current_user_monthly_transactions, 
                                           get_current_user_yearly_transactions,
                                           get_current_user_partitioned_transactions)
from app.sqldb.api.v1.helpers.date_querying_helpers import QueryPartitionRule, QueryPartitionObject
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)


def extract_partition_rule(req):
    partition_rule = None
    if "partition_rule" in req.args:
        try:
            partition_rule = getattr(QueryPartitionRule,  req.args["partition_rule"])
        except:
            raise ValueError("Unknown partion rule")
    return partition_rule

class Transactions(Resource):
    @jwt_required
    def get(self):
        try:
            partition_rule = extract_partition_rule(request)
            if not partition_rule:
                transactions = get_current_user_transactions()
                ts = TransactionSchema(many=True)
            else:
                transactions = get_current_user_partitioned_transactions(partition_rule=partition_rule, return_dict=False)
                ts = PartitionedTransactionSchema(many=True)

            return { 
                'message': 'Found {} transactions'.format(len(transactions)),
                'transactions': ts.dump(transactions)
            }
            
        except:
            return {'message': 'Something went wrong'}, 500


class MonthlyTransactions(Resource):
    @jwt_required
    def get(self, year : str, month : str):
        try:
            partition_rule = extract_partition_rule(request)
            transactions = get_current_user_monthly_transactions(year=year, month=month, partition_rule=partition_rule, return_dict=False)
            ts = PartitionedTransactionSchema(many=True)

            return { 
                'message': 'Found {} transactions'.format(len(transactions)),
                'transactions': ts.dump(transactions)
            }

        except:
            return {'message': 'Something went wrong'}, 500

class YearlyTransactions(Resource):
    @jwt_required
    def get(self, year : str):
        try:
            partition_rule = extract_partition_rule(request)
            transactions = get_current_user_yearly_transactions(year=year, partition_rule=partition_rule, return_dict=False)
            ts = PartitionedTransactionSchema(many=True)

            return { 
                'message': 'Found {} transactions'.format(len(transactions)),
                'transactions': ts.dump(transactions)
            }

        except:
            return {'message': 'Something went wrong'}, 500

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        try:
            # deserialize and receive username and tokens
            urs = UserRegistrationSchema()
            username, access_token, refresh_token = urs.load(data)

            return {
                'message': 'User {} was created'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token 
            }

        except:
            return {'message': 'Something went wrong'}, 500

class UserUpdate(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            # deserialize and receive username and tokens
            eus = EditUserSchema()
            username, access_token, refresh_token = eus.load(data)

            return {
                'message': 'User {} has been updated'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token 
            }

        except:
            return {'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        try:
            # deserialize and receive username and tokens
            urs = UserLoginSchema()
            username, access_token, refresh_token = urs.load(data)

            return {
                'message': 'Logged in as {}'.format(username),
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

class NewTransaction(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            # deserialize and receive username and tokens
            nts = NewTransactionSchema()
            transaction = nts.load(data)
            return {
                'message': 'Transaction {} has been added'.format(transaction.id)
            }
        except:
            return {'message': 'Something went wrong'}, 500

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserUpdate, '/user/update')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(SecretResource, '/secret')
api.add_resource(Transactions, '/transactions')
api.add_resource(YearlyTransactions, '/transactions/<string:year>')
api.add_resource(MonthlyTransactions, '/transactions/<string:year>/<string:month>')
api.add_resource(NewTransaction, '/transaction')