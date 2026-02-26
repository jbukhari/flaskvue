from flask import Flask, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html', user='me')
