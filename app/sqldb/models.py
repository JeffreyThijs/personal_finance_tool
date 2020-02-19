from app import db, login
from flask import current_app
import datetime
import enum
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

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
    prognoses = db.relationship('Prognosis', backref='user', lazy='dynamic')
    last_date_viewed = db.Column(db.DateTime(), default=datetime.date.today())
    email_verified = db.Column(db.Boolean, default=False)
    register_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_prognosis_viewed = db.Column(db.DateTime(), default=datetime.date.today())

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def get_verify_email_token(self, expires_in=60*60*24*7):
        return jwt.encode(
            {'verify_email': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_verify_email_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['verify_email']
        except:
            return
        return User.query.get(id)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.set_password(value)

    @property
    def verified(self):
        return self.email_verified
        
    @verified.setter
    def verified(self, value):
        self.email_verified = value

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
        UNKOWN = 1
        GENERAL = 2
        RECREATIONAL = 3

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    price = db.Column(db.Float(), default=0.0, nullable=False)
    type = db.Column(db.Enum(TransactionType), default=TransactionType.UNKOWN, nullable=False)
    currency = db.Column(db.String(50), default="euro", nullable=False)
    incoming = db.Column(db.Boolean, default=False, nullable=False)
    comment = db.Column(db.String(500), default="placeholder", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def fdate(self):
        return self.date.strftime("%d-%m-%Y")

    @property
    def category(self):
        return Transaction.TransactionType(self.type).name

    @category.setter
    def category(self, value):
        if isinstance(value, str) and not value.isdigit():
            tmp = value.upper()
            self.type = getattr(Transaction.TransactionType, tmp, Transaction.TransactionType.UNKOWN).name
        else:
            self.type = Transaction.TransactionType.coerce(value)

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

    def __str__(self):
        return "(id: {}, price: {}, type: {}, comment: {}, currency: {}, incoming: {}, user_id: {}, date: {}, fdate: {})".format(
            self.id,
            self.price,
            self.type,
            self.comment,
            self.currency,
            self.incoming,
            self.user_id,
            self.date,
            self.fdate
        )

class Prognosis(UserMixin, db.Model):

    class PrognosisOccuranceType(FormEnum):
        DAILY = 1
        MONTHLY = 2
        YEARLY = 3
        ONCE = 4

    __tablename__ = 'prognosis'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(), default=0.0, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    incoming = db.Column(db.Boolean, default=False, nullable=False)
    type = db.Column(db.Enum(PrognosisOccuranceType), default=PrognosisOccuranceType.ONCE, nullable=False)
    comment = db.Column(db.String(500), default="placeholder", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def fdate(self):
        return self.date.strftime("%d-%m-%Y")

    @property
    def occurance(self):
        return Prognosis.PrognosisOccuranceType(self.type).name

    @occurance.setter
    def occurance(self, value):
        self.type = Prognosis.PrognosisOccuranceType.coerce(value)

    @property
    def tag(self):
        return "{}:{}:{}".format(self.occurance.lower(),
                                 "in" if self.incoming else "out",
                                 self.comment)

    def __repr__(self):
        return '<Prognosis {}>'.format(self.id)

    def __str__(self):
        return "(id: {}, amount: {}, type: {}, comment: {}, incoming: {}, user_id: {}, date: {}, fdate: {})".format(
            self.id,
            self.amount,
            self.type,
            self.comment,
            self.incoming,
            self.user_id,
            self.date,
            self.fdate
        )

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)