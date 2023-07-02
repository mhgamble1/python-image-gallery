import psycopg2
import boto3
import os
from werkzeug.utils import secure_filename

connection = None

S3_BUCKET = os.getenv("S3_BUCKET")

def connect():
    global connection
    ig_password_file_path = os.getenv("IG_PASSWD_FILE")
    with open(ig_password_file_path, 'r') as ig_password_file:
        ig_password = ig_password_file.read().strip()
    connection = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        dbname=os.getenv("IG_DATABASE"),
        user=os.getenv("IG_USER"),
        password=ig_password
    )

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    try:
        if not args:
            cursor.execute(query)
        else:
            cursor.execute(query, args)
        return cursor
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        connection.commit()


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

def upload_file(request, user):
    if 'image' not in request.files:
        return "No image file in request"
    image = request.files['image']
    if image.filename == '':
        return 'No selected file'
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        s3.upload_fileobj(image, S3_BUCKET, f'{user.username}/{filename}')
        connect()
        execute("INSERT INTO images (filename, user_id) VALUES (%s, %s)", (filename, user.user_id))
        connection.commit()
        return 'File successfully uploaded'

def delete_image(user, filename):
    execute("delete from images where user_id=%s and filename=%s", (user.user_id, filename))
    s3.delete_object(Bucket=S3_BUCKET, Key=f'{user.username}/{filename}')

def generate_presigned_url(object_name, expiration=3600):
    return s3.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET, 'Key': object_name}, ExpiresIn=expiration)

if __name__ == "__main__":
    list_users_query()
