from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from werkzeug.urls import url_parse
from app.sqldb.models import User
from app import db
from app.auth.email import send_password_reset_email, send_verify_email
from app.auth import bp

def verified_and_authenticated():
    if current_app.config['VERIFIED_LOGIN']:
        return current_user.is_authenticated and current_user.email_verified
    else:
        return current_user.is_authenticated

@bp.route('/login', methods=['GET', 'POST'])
def login():

    if verified_and_authenticated():
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        if current_app.config['VERIFIED_LOGIN']:
            if user and not user.verified:
                send_verify_email(user)
                flash('Please verifiy your email, check your email for instructions!')
                return redirect(url_for('auth.login'))

        flash('Welcome {}!'.format(user.username))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if verified_and_authenticated():
        return redirect(url_for('home.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
                    email=form.email.data,
                    password=form.password.data,
                    verified=False)
        db.session.add(user)
        db.session.commit()

        if current_app.config['VERIFIED_LOGIN']:
            send_verify_email(user)
            flash('Check your email for the instructions to verify your email!')

        # flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if verified_and_authenticated():
        return redirect(url_for('home.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html',
                           title='Reset Password', 
                           form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if verified_and_authenticated():
        return redirect(url_for('home.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)

@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_email(token):

    if verified_and_authenticated():
        return redirect(url_for('home.index'))

    user = User.verify_verify_email_password_token(token)
    if user:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        flash("Email successfully verified!", 'success')
    else:
        flash("Email verification failed, please try again!", 'error')

    return redirect(url_for('home.index'))