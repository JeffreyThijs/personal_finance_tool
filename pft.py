from app.dbutils import add_new_transaction

class PersonalFinanceTool():
    def __init__(self, db_name="db/pft.sqlite"):
        add_new_transaction(price=10.99, comment="more beer")

if __name__ == '__main__':
    ptf = PersonalFinanceTool()
