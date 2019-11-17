import pytest
import datetime
from app.sqldb.models import User, Transaction, Prognosis

@pytest.fixture(scope="module")
def test_users():
    def make_test_users(amount=1):
        users = []
        for i in range(amount):
            users.append(User(id=i,
                              username="test_user", 
                              password="test_password", 
                              email="test@test.test"))
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