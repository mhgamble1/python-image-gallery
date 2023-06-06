from flask import Flask, request, render_template, redirect, url_for
from ..tools.user_admin import list_users, delete_user_query

app = Flask(__name__)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', users=list_users()) 

@app.route("/admin/delete/<username>", methods=['POST'])
def delete(username):
    delete_user_query(username)
    return redirect(url_for('admin'))

@app.route("/admin/addUser", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        add_user_query(username, password, full_name)
        return redirect(url_for('admin'))

    return render_template('add_user.html')

