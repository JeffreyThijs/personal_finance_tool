from marshmallow import Schema, fields, post_load
from app.sqldb.models import User
from app import ma
from app.sqldb.models import Transaction

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
    def make_user(self, data, **kwargs):
        return User(**data)

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

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)