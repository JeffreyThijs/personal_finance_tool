import os
from os.path import join, dirname
from pathlib import Path
import logging

try:
    from dotenv import load_dotenv
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except:
    logging.warn("dotenv not loaded!")

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
    TEMPLATES_AUTO_RELOAD=True