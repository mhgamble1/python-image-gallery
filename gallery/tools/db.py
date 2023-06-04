import psycopg2
import json
from secrets import get_secret_image_gallery

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
    print("{:<10} {:<10} {:<20}".format("username", "password", "full name"))
    print("-------------------------------")
    for row in res:
        print("{:<10} {:<10} {:<20}".format(row[0], row[1], row[2]))

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
    list_users_query()
