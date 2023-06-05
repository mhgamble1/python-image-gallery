from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/admin", methods=['POST'])
def admin():
    return render_template('admin.html', users=list_users()) 


