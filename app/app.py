# Main Flask app. Routes that render templates or static pages are defined
# here. Routes that return data are defined in api.py and imported via
# Blueprint.

import json
from pathlib import Path
from flask import Flask, send_file, render_template, abort
from flask_login import current_user, login_required
from flask_cors import CORS
from flask_pydantic import validate
from app.config import Config
from app.commands import commands
from app.api import API

Config.app = APP = Flask(__name__)
APP.register_blueprint(commands)
APP.register_blueprint(API.blueprint, url_prefix='/api')
CORS(APP)
INTERNAL_JS = getattr(Config, 'INTERNAL_JS', False)
INTERNAL_JS_DIR = getattr(Config, 'INTERNAL_JS_PATH', None) if INTERNAL_JS else None

### Context processor
@APP.context_processor
def supply_js_sources():
    # Where the JS libraries will be loaded from
    
    def relative_path(path):
        # Return path relative to the file with the importmap
        return str(Path(path).relative_to(Path('../templates/base.html').resolve(), walk_up=True)).replace('../app', '') # relative_to requires walkup but js import doesn't support walkup

    return { 
        'vue_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.VUE_FN}') if INTERNAL_JS else Config.VUE_SRC,
        'vue_devtools_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.VUE_DEVTOOLS_FN}') if INTERNAL_JS else Config.VUE_DEVTOOLS_SRC,
        'pinia_src': relative_path(f'{INTERNAL_JS_DIR}/{Config.PINIA_FN}') if INTERNAL_JS else Config.PINIA_SRC
    }

### Routes
@APP.route('/')
def index():
    return render_template('index.html', user='user')

@APP.route('/app')
def main_app():
    return render_template('app.html', user='user')
