import os
from pathlib import Path

home_dir = str(Path.home())
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "o8aBy0lrI7EsC8kpIExQMkznaHXdStMP38y10BtEcJ4Tlz6WlQhApxPafHcuelY6fQN6oUJdE6NNGWBoPzfZxX3hTuuMBZvPrn1vKbZB1OZT9AWu9XqapPRN0xu3cMUV"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    # or 'sqlite:///' + os.getcwd() + '/' + os.path.join('app', 'db', 'pft.sqlite')
    # 'sqlite:///' + os.path.join(home_dir, '.pftdb', 'pft.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False