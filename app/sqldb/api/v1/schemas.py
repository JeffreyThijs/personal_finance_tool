from app import ma
from app.sqldb.models import Transaction

class TransactionSchema(ma.ModelSchema):
    class Meta:
        fields = ("date", "price", "category", "currency", "incoming", "comment")