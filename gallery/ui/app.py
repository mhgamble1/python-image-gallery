from flask import Flask, request, render_template, redirect, url_for
from user_admin import list_users

app = Flask(__name__)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html', users=list_users()) 

@app.route("/admin/delete/<username>", methods=['POST'])
def delete(username):
    delete_user_query(username)
    return redirect(url_for('admin'))
