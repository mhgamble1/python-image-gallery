from . import db
from .user import User
from .user_dao import UserDAO


class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
        result = []
        cursor = db.execute("select user_id,username,password,full_name from users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2], t[3]))
        return result

    def delete_user(self, username):
        db.execute("delete from users where username=%s", (username,))

    def get_user_by_username(self, username):
        cursor = db.execute(
            "select user_id,username,password,full_name from users where username=%s",
            (username,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return User(row[0], row[1], row[2], row[3])

    def get_user_images(self, user):
        result = []
        cursor = db.execute(
            "select filename from images where user_id=%s", (user.user_id,)
        )
        for item in cursor.fetchall():
            result.append(f"{user.username}/{item[0]}")
        return result
