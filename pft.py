
from db.pftdb import PFTdb

class PersonalFinanceTool():
    def __init__(self, db_name="db/pft.sqlite"):
        self.db = PFTdb(db_name)
        self.db.add_new_transaction(price=10.99, comment="more beer")

if __name__ == '__main__':
    ptf = PersonalFinanceTool()
