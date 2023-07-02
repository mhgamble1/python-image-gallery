import psycopg2
import json
import boto3
from werkzeug.utils import secure_filename
from .secrets import get_secret_image_gallery

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_dbname(secret):
    return secret['database_name']

def get_username(secret):
    return secret['username']

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret)) 

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def list_users_query():
    connect()
    res = execute("select * from users")
    return res.fetchall()

def user_exists_query(username):
    connect()
    res = execute("select * from users where username = %s", (username,))
    user_exists = res.fetchone()
    return user_exists is not None

def add_user_query(username, password, full_name, admin):
    execute("insert into users (username, password, full_name, admin) values (%s, %s, %s, %s)",
            (username, password, full_name, admin))
    connection.commit()

def edit_user_query(username, password, full_name, admin):
    if password:
        execute("update users set password = %s where username = %s", (password, username))
    if full_name:
        execute("update users set full_name = %s where username = %s", (full_name, username))
    if admin is not None:
        execute("update users set admin = %s where username = %s", (admin, username))
    connection.commit()

def delete_user_query(username):
    execute("delete from users where username = %s", (username,))
    connection.commit()
    print("\nDeleted.")

def is_admin_query(username):
    res = execute("select admin from users where username = %s", (username,))
    user = res.fetchone()
    return user is not None and user[0]

s3 = boto3.client('s3')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request, user_id):
    if 'image' not in request.files:
        return "No image file in request"
    image = request.files['image']
    if image.filename == '':
        return 'No selected file'
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        s3.upload_fileobj(image, 'edu.au.cc.image-gallery', filename)
        connect()
        execute("INSERT INTO images (filename, user_id) VALUES (%s, %s)", (filename, user_id))
        connection.commit()
        return 'File successfully uploaded'

if __name__ == "__main__":
    list_users_query()
