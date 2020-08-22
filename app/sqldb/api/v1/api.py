import requests
from flask import Blueprint, request, session, current_app
from flask_restplus import Resource, Api
from app import ma, db
from app.sqldb.api.v1.schemas import *
from app.sqldb.models import Transaction, User, RevokedTokenModel
from app.sqldb.api.v1 import _api as api
from app.sqldb.api.v1 import bp
from app.sqldb.api.v1.transactions import (get_current_user_transactions, 
                                           get_current_user_monthly_transactions, 
                                           get_current_user_yearly_transactions,
                                           get_current_user_partitioned_transactions)
from app.sqldb.api.v1.prognoses import get_prognosis_data
from app.sqldb.api.v1.helpers.date_querying_helpers import QueryPartitionRule, QueryPartitionObject
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, 
                                jwt_refresh_token_required, 
                                get_jwt_identity, 
                                get_raw_jwt)


ns = api.namespace('google_auth', description='google_oauth')


oauth_login = api.model('OAuthLogin', {
    'redirect_uri': fields.String(required=True, description='redirect uri')
})


def get_google_provider_cfg():
    return requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()

@ns.route('oauth/login')
class GoogleOAuthLogin(Resource):

    @ns.expect()
    @ns.marshal_with()
    def get(self):

        session['redirect_url'] = request.args.get('ruri', None)

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