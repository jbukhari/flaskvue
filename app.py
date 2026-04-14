from flask import Flask, send_file, render_template
from flask_login import current_user, login_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
Flask.jinja_options.update({'variable_start_string': '[[', 'variable_end_string': ']]'})

@app.route("/")
def home():
    return render_template('app.html', user='me')
