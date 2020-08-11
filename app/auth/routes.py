from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from werkzeug.urls import url_parse
from app.sqldb.models import User
from app import db
from app.auth.email import send_password_reset_email, send_verify_email
from app.auth import bp
import requests
import json

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

def get_google_provider_cfg():
    print(current_app.config['GOOGLE_DISCOVERY_URL'])
    return requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()

@bp.route("/login/google")
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = current_app.oauth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@bp.route("/login/google/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = current_app.oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['GOOGLE_CLIENT_ID'], current_app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    current_app.oauth_client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = current_app.oauth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        # unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        # users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User.query.filter_by(username=users_email).first()

    # Doesn't exist? Add to database
    if not user:
        user = User(username=users_email, email=users_email, email_verified=True)
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('home.index')
    return redirect(next_page)

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