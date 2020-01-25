from flask import Blueprint, request
from flask_restplus import Resource, Api
from app import ma, db
from app.sqldb.api.v1.schemas import TransactionSchema, UserRegistrationSchema, UserLoginSchema
from app.sqldb.models import Transaction, User
from app.sqldb.api.v1 import _api as api
from app.sqldb.api.v1 import bp
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)

@api.route('/transactions')
class Transactions(Resource):
    def get(self):
        transactions = db.session.all()
        ts = TransactionSchema(many=True)
        return ts.dump(transactions)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        try:
            # check username
            user = User.query.filter_by(username=data['username']).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

            # check email
            user = User.query.filter_by(email=data['email']).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

            # deserialize
            urs = UserRegistrationSchema()
            user = urs.load(data)

            # add user to db
            db.session.add(user)
            # db.session.commit()

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
            # check username
            user = User.query.filter_by(username=data['username']).first()
            if user is None:
                raise ValidationError('User does not exist')

            # check password
            if not user.check_password(data['password']):
                raise ValidationError('Wrong password')

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
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
# class AllUsers(Resource):
#     def get(self):
#         return {'message': 'List of users'}

#     def delete(self):
#         return {'message': 'Delete all users'}
      
      
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
# api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/secret')