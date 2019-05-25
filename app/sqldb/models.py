from app import db, login
import datetime
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class FormEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(choice, choice.name.title()) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    last_date_viewed = db.Column(db.DateTime(), default=datetime.date.today())

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

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

class Transaction(UserMixin, db.Model):

    class TransactionType(FormEnum):
        UNKNOWN = 1
        GENERAL = 2
        RECREATIONAL = 3

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    price = db.Column(db.Float(), default=0.0, nullable=False)
    type = db.Column(db.Enum(TransactionType), default=TransactionType.UNKNOWN, nullable=False)
    currency = db.Column(db.String(50), default="euro", nullable=False)
    incoming = db.Column(db.Boolean, default=False, nullable=False)
    comment = db.Column(db.String(500), default="placeholder", nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

    def __str__(self):
        return "(id: {}, price: {}, type: {}, comment: {}, currency: {}, incoming: {}, user_id: {}, date: {})".format(
            self.id,
            self.price,
            self.type,
            self.comment,
            self.currency,
            self.incoming,
            self.user_id,
            self.date
        )
