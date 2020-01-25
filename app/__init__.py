from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_caching import Cache
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
bootstrap = Bootstrap()
mail = Mail()
cache = Cache()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
ma = Marshmallow()
jwt_manager = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db=db)
    login.init_app(app)
    ma.init_app(app)
    jwt_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.sqldb.api.v1 import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from app.core.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.core.overview import bp as overview_bp
    app.register_blueprint(overview_bp, url_prefix='/core/overview')

    from app.core.tax import bp as tax_bp
    app.register_blueprint(tax_bp, url_prefix='/core/tax')

    from app.core.prognosis import bp as prognosis_bp
    app.register_blueprint(prognosis_bp, url_prefix='/core/prognosis')

    return app

from app.sqldb import models
from app.sqldb.api.v1 import api as _api