import psycopg2

db_host = "m2-database.c9vwiewrcstl.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"
connection = None

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result [:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password()) 

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


if __name__ == "__main__":
    list_users_query()
