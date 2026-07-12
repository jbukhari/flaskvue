# Routes are declared using both conventional Flask declaration and Flask-RESTX
# declaration

import os, json, requests
from pathlib import Path
from flask import Flask, send_file, render_template, jsonify, request, Response, abort
from flask_login import current_user, login_required
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from flask_pydantic import validate
from app.config import Config
from app import models
from app import commands

APP = Flask(__name__)
Config.app = APP
CORS(APP)
INTERNAL_JS = getattr(Config, 'INTERNAL_JS', False)
INTERNAL_JS_DIR = getattr(Config, 'INTERNAL_JS_PATH', None) if INTERNAL_JS else None

@APP.context_processor
def supply_js_sources():
    # Where the JS libraries will be loaded from
    
    def relative_path(path):
        # Return path relative to the file with the importmap
        return str(Path(path).relative_to(Path('../templates/base.html').resolve(), walk_up=True)).replace('../app', '')

    return { 
        'vue_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.VUE_FN}') if INTERNAL_JS else Config.VUE_SRC,
        'vue_devtools_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.VUE_DEVTOOLS_FN}') if INTERNAL_JS else Config.VUE_DEVTOOLS_SRC,
        'pinia_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.PINIA_FN}') if INTERNAL_JS else Config.PINIA_SRC
    }

    

@APP.cli.command("download-js-modules")
def download_js_modules():
    """Download JS modules for internal use."""

    js_modules = {
        Config.VUE_FN: Config.VUE_SRC,
        Config.VUE_DEVTOOLS_FN: Config.VUE_DEVTOOLS_SRC,
        Config.PINIA_FN: Config.PINIA_SRC
    }

    js_dir = Config.INTERNAL_JS_PATH
    os.makedirs(js_dir, exist_ok=True)

    for filename, url in js_modules.items():
        response = requests.get(url)

        if response.status_code == 200:
            with open(os.path.join(js_dir, filename), 'wb') as f:
                f.write(response.content)

            print(f"Downloaded {filename} to {js_dir}")
        else:
            print(f"Failed to download {filename} from {url}")
    
### Conventional routes
@APP.route('/')
def index():
    return render_template('index.html', user='user')

@APP.route('/app')
def main_app():
    return render_template('app.html', user='user')

### API routes
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
