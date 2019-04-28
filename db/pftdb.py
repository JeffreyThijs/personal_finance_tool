import os
from db.model import Base, Transaction
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class PFTdb():

    def __init__(self, name="pft.sqlite"):
        self.name = name
        self.engine = None
        self.session_maker = None
        self.session = None
        self.init_database()

    def __del__(self):
        if self.session:
            self.session.close()

    def init_database(self):
        create_db = False if os.path.exists(self.name) else True

        self.engine = create_engine('sqlite:///' + self.name)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)

        if(create_db):
            print("DB {} does not exist, creating new one...".format(self.name))
            Base.metadata.create_all(self.engine)
        else:
            Base.metadata.bind = self.engine

        self.session = self.session_maker()

    def add_new_transaction(self, price, comment):

        transaction = Transaction(price=price, comment=comment)
        print("Adding new transaction: {}".format(transaction))
        self.session.add(transaction)
        self.session.commit()
