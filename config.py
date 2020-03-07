import os
from os.path import join, dirname
from pathlib import Path
import logging
import tempfile

try:
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except:
    logging.warn("dotenv not loaded!")

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATION')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CACHE_TYPE = os.environ.get("CACHE_TYPE") 
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT") or 300)
    if os.environ.get("SEND_FILE_MAX_AGE_DEFAULT"): 
        SEND_FILE_MAX_AGE_DEFAULT = os.environ.get("SEND_FILE_MAX_AGE_DEFAULT")
    TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD")
    VERIFIED_LOGIN = bool(os.environ.get("VERIFIED_LOGIN") == "True")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = os.environ.get("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class TestConfig(object):
    SECRET_KEY = 'bad_secret_key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'simple'
    MAIL_PORT = 25
    MAIL_SERVER = "127.0.0.1"
    MAIL_USERNAME = "test"
    MAIL_PASSWORD = "test"
    VERIFIED_LOGIN = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = os.environ.get("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']