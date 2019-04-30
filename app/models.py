from app import db
import datetime

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    price = db.Column(db.Float())
    comment = db.Column(db.String(500))
    type = db.Column(db.String(50))

    def __str__(self):
        return "(date: %s, price: %f, type: %s, comment: %s)" % (
            "test",
            self.price,
            self.type,
            self.comment,
        )
