from app.sqldb.models import Transaction

def test_new_transaction(test_transactions):
    new_transaction = test_transactions(amount=1)[0]
    assert new_transaction.id == 0
    assert new_transaction.price == 555.0
    assert new_transaction.incoming == False
    assert new_transaction.category == "GENERAL"
    assert new_transaction.type == Transaction.TransactionType.GENERAL
    new_transaction.category = Transaction.TransactionType.RECREATIONAL.value
    assert new_transaction.category == Transaction.TransactionType.RECREATIONAL.name
    assert new_transaction.comment == "placeholder"