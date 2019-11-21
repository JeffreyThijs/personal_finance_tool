from flask import render_template, current_app
from app.tools.mailutils import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[PFT] Reset Your Password',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',  user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

def send_verify_email(user):
    token = user.get_verify_email_token()
    send_email('[PFT] Verifiy Your Account',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/verify_email.txt',  user=user, token=token),
               html_body=render_template('email/verify_email.html', user=user, token=token))