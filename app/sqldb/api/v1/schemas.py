from marshmallow import Schema, fields, post_load, pre_load
from flask_login import current_user
from app.sqldb.models import User
from app import ma, db
from app.sqldb.models import Transaction
from flask_login import login_user
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)

class TransactionSchema(ma.ModelSchema):
    class Meta:
        fields = ("date", "price", "category", "currency", "incoming", "comment")

class UserRegistrationSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()

    @pre_load
    def check_user(self, data, **kwargs):
        # check username
        user = User.query.filter_by(username=data['username']).first()
        if user is not None:
            raise ValueError('Please use a different username.')

        # check email
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            raise ValueError('Please use a different email address.')

    @post_load
    def make_user_and_tokens(self, data, **kwargs):
        
        # make new user and add it to db
        user = User(**data)
        db.session.add(user)
        db.session.commit()

        # login user
        login_user(user)

        # create tokens
        access_token = create_access_token(identity = user.username)
        refresh_token = create_refresh_token(identity = user.username)

        return user.username, access_token, refresh_token

class UserLoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @pre_load
    def check_user(self, data, **kwargs):
        # check username
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            raise ValueError('User does not exist')

        # check password
        if not user.check_password(data['password']):
            raise ValueError('Wrong password')

        # login user
        login_user(user)

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