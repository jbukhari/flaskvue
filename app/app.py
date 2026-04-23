# Routes are declared using both conventional Flask declaration and Flask-RESTX
# declaration

import json
from flask import Flask, send_file, render_template, jsonify, request, Response, abort
from flask_login import current_user, login_required
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from flask_pydantic import validate
from app.config import Config
from app import models

### Conventional routes
APP = Flask(__name__)
CORS(APP)

@APP.route('/')
def index():
    return render_template('index.html', user='user')

@APP.route('/app')
def main_app():
    return render_template('app.html', user='user')

### API
# Flask-RESTX
API = Api(APP, doc='/api')
NS = API.namespace('api', description='App API')

# All routes defined below come after "api/", set by the namespace object
@NS.route('')
class Doc(Resource):
    @NS.doc(description='API Documentation')
    def get(self):
        # Placeholder for the Swagger doc provided by Flask-RESTX, set using
        # the "doc" argument to the Api object.
        return {'message': 'The documentation is supposed to be supplied here by Flask-RESTX.'}

@NS.route('/records')
class Records(Resource):
    @NS.doc(description='List records')
    def get(self):
        data = [{'id': 1}]
        return (jsonify([]))
    
    @NS.doc(description='Create record')
    @NS.expect(models.Record.model())
    def post(self):
        data = json.loads(request.data)
        
        if models.Record.model_validate(data):
            return Response(status=201)
        
        abort(400)
    
@NS.route('/record')
class Record(Resource):
    @NS.doc(description='Get record')
    def get(self):
        data = {'id': 1}
        return (data)
