class User:
    def __init__(self, user_id, username, password, full_name):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name

    def __repr__(self):
        return (
            "User with username "
            + self.username
            + " password: "
            + self.password
            + " full name: "
            + self.full_name
        )
