from typing import List
from flask import render_template, current_app
from flask_login import current_user, login_required
from app.core.home import bp
from app.core.home.charts import get_bar_charts_data, get_donut_charts_data, get_line_charts_data
from app.sqldb.api.v1.transactions import get_user_transactions

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    donut_data = get_donut_charts_data()
    bar_data = get_bar_charts_data()
    line_data = get_line_charts_data()
    
    from app import db
    from app.sqldb.models import Transaction
    
    all_data: List[Transaction] = db.session.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    all_data = [dict(date=x.date, 
                     user_email=x.user.email,
                     price=x.price,
                     comment=x.comment,
                     incoming=x.incoming) for x in all_data]

    return render_template('/core/home/index.html',
                            all_data=all_data,
                            line_data=line_data,
                            bar_data=bar_data,
                            donut_data=donut_data)