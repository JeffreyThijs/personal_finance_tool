from marshmallow import Schema, fields, post_load, pre_load
from flask_jwt_extended import current_user
from app.sqldb.models import User, Transaction
from app import ma, db
from app.sqldb.models import Transaction
from flask_login import login_user
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)
import datetime

class TransactionSchema(ma.ModelSchema):
    class Meta:
        model = Transaction
        fields = ("date", "price", "category", "currency", "incoming", "comment")

class UserRegistrationSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()

    @pre_load
    def check_user(self, data, many, **kwargs):
        # check username
        user = User.query.filter_by(username=data['username']).first()
        if user is not None:
            raise ValueError('Please use a different username.')

        # check email
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            raise ValueError('Please use a different email address.')

        return data

    @post_load
    def make_user_and_tokens(self, data, **kwargs):
        
        # make new user and add it to db
        user = User(**data)
        db.session.add(user)
        db.session.commit()

        # create tokens
        access_token = create_access_token(identity = user.username)
        refresh_token = create_refresh_token(identity = user.username)

        return user.username, access_token, refresh_token

class UserLoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @pre_load
    def check_user(self, data, many, **kwargs):
        # check username
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            raise ValueError('User does not exist')

        # check password
        if not user.check_password(data['password']):
            raise ValueError('Wrong password')
        
        return data

    @post_load
    def make_user_tokens(self, data, **kwargs):
        username = data['username']
        access_token = create_access_token(identity = username)
        refresh_token = create_refresh_token(identity = username)
        return username, access_token, refresh_token

class EditUserSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def edit_user(self, data, **args):
        pass
    
class PartitionedTransactionSchema(Schema):
    year = fields.String()
    month = fields.String()
    transactions = fields.List(fields.Nested(TransactionSchema()))

class NewTransactionSchema(Schema):
    date = fields.Str()
    price = fields.Float()
    category = fields.Integer()
    currency = fields.String()
    incoming = fields.Boolean()
    comment = fields.String()

    @post_load
    def format_data(self, data, many, **kwargs):
        # check username
        data["date"] = datetime.datetime.strptime(data["date"], '%d/%m/%Y')
        transaction = Transaction(user_id=current_user.id, **data)
        db.session.add(transaction)
        db.session.commit()
        return transaction