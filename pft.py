from app.dbutils import add_new_transaction
from tools.dateutils import convert_to_datetime

class PersonalFinanceTool():
    def __init__(self, db_name="db/pft.sqlite"):
        dt = convert_to_datetime("30", "06", "1994")
        add_new_transaction(price=10.99, comment="more beer", date=dt)

if __name__ == '__main__':
    ptf = PersonalFinanceTool()
