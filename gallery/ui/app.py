from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/admin", methods=['POST'])
def admin():
    return render_template('admin.html', users=list_users()) 

@app.route("/admin/delete/<username>", methods=['POST'])
def delete(username):
    delete_user_query(username)
    return redirect(url_for('admin'))
