# Routes are declared using both conventional Flask declaration and Flask-RESTX
# declaration

import os, json
from pathlib import Path
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
EXTERNAL_JS = not os.environ.get('EXTERNAL_JS') or False # default to loading JS from external sources
INTERNAL_JS_PATH = '../static/js' 

@APP.context_processor
def supply_js_sources():
    return {
        'vue_src': 'https://unpkg.com/vue@3.5.29/dist/vue.esm-browser.js' if EXTERNAL_JS else f'{INTERNAL_JS_PATH}/vue_3.5.29_esm-browser.js',
        'vue_devtools_src': 'https://unpkg.com/@vue/devtools-api@8.1.1/dist/vue-devtools-api.esm-browser.js' if EXTERNAL_JS else f'{INTERNAL_JS_PATH}/vue-devtools-api_8.1.1_esm-browser.js',
        'pinia_src': 'https://unpkg.com/pinia@3.0.4/dist/pinia.esm-browser.js' if EXTERNAL_JS else f'{INTERNAL_JS_PATH}/pinia_3.0.4_esm-browser.js'
    }

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
