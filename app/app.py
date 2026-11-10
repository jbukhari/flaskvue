# Main Flask app. Routes that render templates or static pages are defined
# here. Routes that return data are defined in api.py and imported via
# Blueprint.

import json
from secrets import token_hex
from pathlib import Path
from flask import Flask, send_file, render_template, abort, request, Response, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from app.config import Config
from app.db import DB, User
from app.commands import commands
from app.api import API

### Setup
Config.app = APP = Flask(__name__)
APP.register_blueprint(commands)
APP.register_blueprint(API.blueprint, url_prefix='/api')
APP.secret_key = Config.SECRET_KEY
CORS(APP)
INTERNAL_JS = getattr(Config, 'INTERNAL_JS', False)
INTERNAL_JS_DIR = getattr(Config, 'INTERNAL_JS_PATH', None) if INTERNAL_JS else None
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    # Implementation required by Flask-Login
   return User.from_query({'userId': user_id})

@APP.context_processor
def _context():
    # Fields in the returned dict are available to all Jinja templates. This
    # allows internal JavaScript source location to be set in Config.
    # https://flask.palletsprojects.com/en/stable/templating/#context-processors
    
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
    return render_template('index.html')

@APP.route('/app')
def main_app():
    return render_template('app.html', user='user')

@APP.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'Already logged in'
    
    if Config.TESTING or Config.DEV:
        APP.secret_key = token_hex(24)
    elif not Config.SECRET_KEY:
        raise Exception('Environment variable "SECRET_KEY" required  to start user sessions')
    
    if Config.DEV and not User.from_query({'userId': 'dev'}):
        # Create a dev user if the db is starting blank
        User.add_user('dev', 'dev')

    if request.method == 'GET':
        return render_template('login.html')

    # POST
    data = request.form.to_dict()
    uid = data.get('userId')
    password = data.get('password')
    
    if user := User.from_query({'userId': uid}):
        if not user.login(password):
            abort(401, 'Incorrect password')

        this = url_for("login", _external=True)
        ref = request.referrer
            
        return redirect(ref if ref and (ref != this) else url_for('index'))
    else:
        abort(404, 'User not found')

@APP.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))