from app import jwt_manager, db
from app.sqldb.models import RevokedTokenModel, User

@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

@jwt_manager.user_loader_callback_loader
def user_loader_callback(username):
    return db.session.query(User).filter(User.username == username).one_or_none()

@jwt_manager.user_loader_error_loader
def custom_user_error_loader(user_id):
    return {'message': 'user could not be loaded'}, 500