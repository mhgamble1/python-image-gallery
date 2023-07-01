import json
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, session
from ..tools.db import list_users_query, delete_user_query, add_user_query, edit_user_query

from ..tools.user import User
from ..tools.postgres_user_dao import PostgresUserDAO
from ..tools.db import connect
from ..tools.secrets import get_secret_flask_session

app = Flask(__name__)
secret = get_secret_flask_session()
secret_dict = json.loads(secret)
app.secret_key = secret_dict["secret_key"]

connect()

def get_user_dao():
    return PostgresUserDAO()

def check_admin():
    return 'username' in session and session['username'] == 'test'

# admin
def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated

@app.route("/admin", methods=['GET', 'POST'])
@requires_admin
def admin():
    if not check_admin():
        return redirect('/login')
    return render_template('admin.html', users=list_users_query()) 

@app.route("/admin/delete/<username>", methods=['POST'])
@requires_admin
def delete(username):
    delete_user_query(username)
    return redirect(url_for('admin'))

@app.route("/admin/addUser", methods=['GET', 'POST'])
@requires_admin
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        add_user_query(username, password, full_name)
        return redirect(url_for('admin'))

    return render_template('add_user.html')

@app.route("/admin/edit/<username>", methods=['GET', 'POST'])
@requires_admin
def edit(username):
    if request.method == 'POST':
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        edit_user_query(username, password, full_name)
        return redirect(url_for('admin'))

    return render_template('edit_user.html', username=username)

# main routes
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/invalidLogin")
def invalidLogin():
    return "Invalid"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect("/debugSession")
    else:
        return render_template('login.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route("/images", methods=['GET', 'POST'])
def images():
    return render_template('images.html')

# sessions
@app.route("/debugSession")
def debugSession():
    result = ""
    for key,value in session.items():
        result += key+"->"+str(value)+"<br />"
    return result

