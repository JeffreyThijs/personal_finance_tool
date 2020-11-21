# Personal Finance Tool

A simple web application to track your personal finances.

# Deploy

This application can be deployed easily on Heroku, hereby specify the following parameters in your `.env` file:

```
SECRET="VERYSECRET"
DATABASE_URL=postgresql://username:password@database
GOOGLE_OAUTH_CLIENT_ID="YOURGOOGLECLIENTID"
GOOGLE_OAUTH_CLIENT_SECRET="YOURGOOGLECLIENTSECRET"
MAIL_USERNAME="YOURMAILUSERNAME"
MAIL_PASSWORD="YOURMAILPASSWORD"
MAIL_FROM="your@mail.com"
MAIL_SERVER="your.mailserver.com"
```

To set these vars via the Heroku CLI:

```
heroku config:push -f .env -o
```