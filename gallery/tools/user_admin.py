from db import list_users_query

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

def add_user():
    print("\nadding user")
    print(add_user_prompt())

def edit_user():
    print("\nediting user")

def delete_user():
    print("\ndeleting user")

def quit():
    print("\nquitting")
    exit(0)

def validation_warning():
    print("\nplease enter a number 1-5")

def add_user_prompt():
    username = input("Username> ")
    password = input("Password> ")
    full_name = input("Full name> ")
    return username, password, full_name

def main():
    while True:
        menu()
        selection = int(input("Enter command> "))
        if selection == 1:
            list_users() 
        elif selection == 2:
            add_user() 
        elif selection == 3:
            edit_user()    
        elif selection == 4:
            delete_user() 
        elif selection == 5:
            quit() 
        else:
            validation_warning()


if __name__ == "__main__":
    main()
