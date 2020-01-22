from flask_restplus import Resource
from app import api, ma

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}