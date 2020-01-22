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

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserLoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)