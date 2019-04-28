import os
from db.model import Base, Transaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class PersonalFinanceTool():
    def __init__(self, db_name="db/pft.sqlite"):
        self.db_name = db_name
        self.engine = None
        self.session_maker = None
        self.init_database()

    def init_database(self):

        create_db = False if os.path.exists(self.db_name) else True

        self.engine = create_engine('sqlite:///' + self.db_name)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)

        if(create_db):
            print("DB {} does not exist, creating new one...".format(self.db_name))
            Base.metadata.create_all(self.engine)
        else:
            Base.metadata.bind = self.engine

    def add_new_transaction(self, price, comment):
        session = self.session_maker()
        transaction = Transaction(price=price, comment=comment)
        session.add(transaction)
        session.commit()
        session.close()

if __name__ == '__main__':
    ptf = PersonalFinanceTool()
    ptf.add_new_transaction(price=10.99, comment="some beer")
