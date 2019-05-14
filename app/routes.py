from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm, TransactionForm, TranactionButton, TaxForm
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, dt_parse
from app.tools.taxutils import calc_net_wage
from app.tools.plotutils import test_plot, _plot
from app.dbutils import add_new_transaction
from werkzeug.urls import url_parse
from app.models import User
from sqlalchemy import and_
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Plots')

@app.route('/', methods=['GET', 'POST'])
@app.route('/monthly_overview', methods=['GET', 'POST'])
@login_required
def monthly_overview():
    new_transaction = TranactionButton()
    if new_transaction.validate_on_submit():
        return redirect(url_for('entry'))

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    current_date_view = dt_parse(current_user.last_date_viewed)

    current_month_view, current_year_view = str(current_user.last_date_viewed.month), str(current_user.last_date_viewed.year)
    transactions = filter_on_MonthYear(transactions, "date", current_month_view, current_year_view)

    balance = round(sum(t.price for t in transactions if t.incoming) - sum(t.price for t in transactions if not t.incoming), 2)

    return render_template('monthly_overview.html',
                           new_transaction=new_transaction,
                           title='Home',
                           transactions=transactions,
                           balance=balance,
                           current_date_view=current_date_view)


@app.route('/makeplots', methods=['GET'])
@login_required
def make_plots():
    dates = []
    current_date = None
    current_balance = 0.0
    balance_history = []

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)
    for t in transactions:
        if t.incoming:
            current_balance += t.price
        else:
            current_balance -= t.price

        current_date = t.date

        if len(dates) == 0 or current_date != dates[-1:]:
            dates.append(current_date)
            balance_history.append(current_balance)

    bytes_obj = _plot(balance_history,
                      x=dates,
                      title='Balance History',
                      xlabel='Date',
                      ylabel='Balance',
                      figure_number=0,
                      filetype='png')

    return send_file(bytes_obj, attachment_filename='plot.png', mimetype='image/png')

# @app.route('/plots')
# @login_required
# def get_plots():
#     return render_template('plots.html', title='Plots')

@app.route('/next_month', methods=['GET', 'POST'])
@login_required
def next_month():
    current_month = current_user.last_date_viewed.month
    new_month = _next_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(month=new_month)
    if current_month == 12:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(year=current_year+1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))

@app.route('/previous_month', methods=['GET', 'POST'])
@login_required
def previous_month():
    current_month = current_user.last_date_viewed.month
    new_month = _previous_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(month=new_month)
    if current_month == 1:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(year=current_year-1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))

@app.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form = TransactionForm()
    if form.validate_on_submit():
        add_new_transaction(price=form.price.data,
                            date=form.date.data,
                            comment=form.comment.data,
                            user_id=current_user.id,
                            incoming=form.incoming.data)
        return redirect(url_for('monthly_overview'))
    return render_template('entry.html', title='Entry', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tax', methods=['GET', 'POST'])
@login_required
def tax():
    form = TaxForm()
    net_wage = -1
    if form.validate_on_submit():
        net_wage = calc_net_wage(form.gross_wage.data)
    return render_template('tax.html', title='Tax', form=form, net_wage=net_wage)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
