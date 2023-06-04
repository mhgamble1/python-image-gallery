from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/admin")
def admin():
    pass
