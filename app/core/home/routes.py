from flask import render_template, current_app
from flask_login import current_user, login_required
from app.core.home import bp
from app.core.home.charts import get_bar_charts_data, get_donut_charts_data, get_line_charts_data
from app.sqldb.transactions import get_user_transactions

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    transactions = get_user_transactions()
    donut_data = get_donut_charts_data(transactions)
    bar_data = get_bar_charts_data(transactions)
    line_data = get_line_charts_data(transactions)

    return render_template('/core/home/index.html', 
                            line_data=line_data,
                            bar_data=bar_data,
                            donut_data=donut_data)