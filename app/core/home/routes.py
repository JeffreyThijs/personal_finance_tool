from flask import render_template
from flask_login import current_user, login_required
from app.core.home import bp
from app.core.home.charts import get_bar_charts_data, get_donut_charts_data, get_line_charts_data

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    donut_data = get_donut_charts_data(transactions)
    bar_data = get_bar_charts_data(transactions)
    line_data = get_line_charts_data(transactions)

    return render_template('index.html', 
                            line_data=line_data,
                            bar_data=bar_data,
                            donut_data=donut_data)