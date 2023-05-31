from db import list_users_query, user_exists_query, add_user_query, edit_user_query, delete_user_query

def menu():
    print()
    print("1) List users")
    print("2) Add user")
    print("3) Edit user")
    print("4) Delete user")
    print("5) Quit")

def list_users():
    print("\nlisting users")
    list_users_query()

def add_user_prompt():
    print()
    username = input("Username> ")

    if user_exists_query(username):
        print(f"\nError: user with username {username} already exists")
        return None, None, None

    password = input("Password> ")
    full_name = input("Full name> ")
    return username, password, full_name

def edit_user_prompt():
    print()
    username = input("Username to edit> ")

    if not user_exists_query(username):
        print("\nNo such user.")
        return None, None, None

    password = input("New password (press enter to keep current)>")
    full_name = input("New full name (press enter to keep current)>")
    return username, password, full_name

def delete_user_prompt():
    print()
    username = input("Enter username to delete> ")

    if not user_exists_query(username):
        print("\nNo such user.")
        return None

    confirmation = input(f"Are you sure that you want to delete {username}? ")
    if confirmation in ["Yes", "YES", "yes", "Y", "y"]:
        return username
    else:
        return None

def quit():
    print("\nBye.")
    exit(0)

def validation_warning():
    print("\nPlease enter a number 1-5")


def main():
    while True:
        menu()
        try:
            selection = int(input("Enter command> "))
        except ValueError:
            validation_warning()
            continue

        if selection == 1:
            list_users() 
        elif selection == 2:
            username, password, full_name = add_user_prompt()
            if username is None:
                continue
            add_user_query(username, password, full_name)
        elif selection == 3:
            username, password, full_name = edit_user_prompt()    
            if username is None:
                continue
            edit_user_query(username, password, full_name)
        elif selection == 4:
            username = delete_user_prompt()
            if username is None:
                continue
            delete_user_query(username) 
        elif selection == 5:
            quit() 
        else:
            validation_warning()


if __name__ == "__main__":
    main()
