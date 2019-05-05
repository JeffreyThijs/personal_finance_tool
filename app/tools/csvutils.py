import xlrd
import csv
import os
import numpy as np
import datetime
from app.dbutils import _add_new_transaction
from app.models import User
from app import db

def csv_from_excel(src, sheet, dst):
    wb = xlrd.open_workbook(src)
    sh = wb.sheet_by_name(sheet)
    csv_file = open(dst, 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()

def parse_transaction_csv(username, src, sheet, dst="tmp.csv", delimiter=','):

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        raise ValueError("user does not exist")

    def calc_date(days_since_epoch : int) -> datetime:
        return datetime.date(1900, 1, 1) + datetime.timedelta(days=days_since_epoch-2)

    if not os.path.exists(src):
        raise ValueError("src path does not exist!")

    csv_from_excel(src=src,
                   sheet=sheet,
                   dst=dst)

    with open(dst) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            days_since_epoch, comment, price, incoming = row
            date = calc_date(int(float(days_since_epoch)))
            price = float(price)
            incoming = bool(float(incoming))


            # assert(isinstance(date, datetime))
            assert(isinstance(price, float))
            assert(isinstance(comment, str))
            assert(isinstance(user.id, int))
            assert(isinstance(incoming, bool))

            _add_new_transaction(price=price,
                                 date=date,
                                 comment=comment,
                                 user_id=user.id,
                                 incoming=incoming)

    os.remove(dst)

# runs the csv_from_excel function:

parse_transaction_csv(username="jthijs",
                      src="/home/jthijs/Documents/administration/Financiën.xlsx",
                      sheet="csv",
                      dst="test.csv")
