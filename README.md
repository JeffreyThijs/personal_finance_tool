# Personal Finance Tool

A simple web application to track your personal finances.

![master](https://github.com/JeffreyThijs/personal_finance_tool/workflows/.github/workflows/pft.yml/badge.svg)
[![codecov](https://codecov.io/gh/JeffreyThijs/personal_finance_tool/branch/master/graph/badge.svg?token=1QBMYLET49)](https://codecov.io/gh/JeffreyThijs/personal_finance_tool)

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
