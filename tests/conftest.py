import pytest
import datetime
from app.sqldb.models import User, Transaction, Prognosis
from config import TestConfig
from app import create_app, db
from faker import Faker
from app.tools.helpers_classes import AttrDict
from tests.helpers.fake_smtp import FakeSMTPServer
import asyncore

@pytest.fixture(scope="module")
def test_users():
    def make_test_users(amount=1):

        users = [User(id=0,
                      username="test_user", 
                      password="test_password", 
                      email="test@test.test")]

        for i in range(1, amount):
            f = Faker()
            profile = AttrDict(f.profile())
            users.append(User(id=i,
                              verified=True,
                              username=profile.username, 
                              password=profile.job, 
                              email=profile.mail))
        return users
    return make_test_users

@pytest.fixture(scope="module")
def test_transactions():
    def make_test_transactions(amount=1):
        transactions = []
        for i in range(amount):
            transactions.append(Transaction(id=i,
                                            price=555.0,
                                            incoming=False,
                                            type=Transaction.TransactionType.GENERAL,
                                            date=datetime.datetime.now(),
                                            currency="euro",
                                            comment="placeholder"))
        return transactions
    return make_test_transactions

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database(test_users):

    # create users
    new_users = test_users(amount=10)

    # Create the database and the database table
    db.create_all()

    # Insert user data
    for user in new_users:
        db.session.add(user)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()

@pytest.fixture(scope='module')
def init_smtp():
    smtp_server = FakeSMTPServer(('localhost', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()