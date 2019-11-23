# Personal Finance Tool

A simple web application to track your personal finances. 

# Deploy

This application can be deployed easily on Heroku, hereby specify the following parameters in your `.env` file:

```
SECRET_KEY = 'averysecretkey'
DATABASE_URL = 'urltoyourpostgresdb'
SQLALCHEMY_TRACK_MODIFICATION = False
MAIL_SERVER = 'yourmailserver'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'emailusername'
MAIL_PASSWORD = 'emailpassword'
CACHE_TYPE = 'cachemethodofinterest'
CACHE_DEFAULT_TIMEOUT = 300
```

To set these vars via the Heroku CLI:

```
heroku config:push -f .env -o
```