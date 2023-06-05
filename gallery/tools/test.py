import psycopg2
import json
from secrets import get_secret_image_gallery

connection = None

def get_secret():
    try:
        print("Getting secret...")
        jsonString = get_secret_image_gallery()
        print(f"Secret obtained: {jsonString}")
        return json.loads(jsonString)
    except Exception as e:
        print(f"Failed to get or parse secret: {e}")
        return None

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
    try:
        secret = get_secret()
        print(f"Secret: {secret}")  # This will print your secret, be careful not to expose sensitive info
        connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), 
                                      user=get_username(secret), password=get_password(secret))
        print("Database connection successful.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}") 

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
    try:
        res = execute("select * from users")
        users = res.fetchall()
        print(f"Users: {users}")  # This will print the list of users
        return users
    except Exception as e:
        print(f"Failed to fetch users: {e}")

def user_exists_query(username):
    connect()
    res = execute("select * from users where username = %s", (username,))
    user_exists = res.fetchone()
    return user_exists is not None

def add_user_query(username, password, full_name):
    execute("insert into users (username, password, full_name) values (%s, %s, %s)",
            (username, password, full_name))
    connection.commit()

def edit_user_query(username, password, full_name):
    if password:
        execute("update users set password = %s where username = %s", (password, username))
    if full_name:
        execute("update users set full_name = %s where username = %s", (full_name, username))
    connection.commit()

def delete_user_query(username):
    execute("delete from users where username = %s", (username,))
    connection.commit()
    print("\nDeleted.")

if __name__ == "__main__":
    print("starting")
    for user in list_users_query():
        print(user)
