from app import db
import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return "(username: {}, email: {}".format(
            self.username,
            self.email
        )

class Transaction(db.Model):

    class TransactionType(enum.Enum):
        GENERAL = 1
        RECREATIONAL = 2
        UNKOWN = 3

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    price = db.Column(db.Float())
    type = db.Column(db.Enum(TransactionType))
    currency = db.Column(db.String(50))
    incoming = db.column(db.Boolean)
    comment = db.Column(db.String(500))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="transactions")

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

    def __str__(self):
        return "(price: {}, type: {}, comment: {}".format(
            self.price,
            "null",
            self.comment
        )
