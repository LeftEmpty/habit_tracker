import os
from sqlite_rx.client import SQLiteClient # type: ignore
from .sql_controller import db_create_user, db_login_user
import getpass

#globals
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def create_user(sql_client: SQLiteClient) -> int | None:
    clear()

    print("Please enter your credentials:\n\n")

    display_name: str = input("Your Display Name:")
    username: str = input("Your username:")
    password: str = getpass.getpass("Your new password:") 
    
    user_id: int | None = db_create_user(
            sql_client=sql_client,
            display_name=display_name,  # Replace with actual SQLite client instance
            username=username,
            password=password
    )
    return user_id
    

def login_user(sql_client: SQLiteClient) -> int | None:

    #User selection / creation
    while True:
        clear()
        #Login
        print("Welcome to the Habit Tracker CLI!")
        print("Do you want to: \n")
        print("1. Log in")
        print("2. Create a new user")
        print("3. Exit\n")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            clear()
            print("Please log in to continue.\n\n")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            user_id = db_login_user(
                sql_client=sql_client,
                username=username,
                password=password
            )

            if user_id:
                clear()
                print(f"Current user is {user_id}")
                return user_id

            print("User not found or wrong credentials\n")

        elif choice == "2":
            create_user(sql_client)

        elif choice == "3":
            print("Exiting...")
            return  # Exit the function
        else:
            print("Invalid choice. Please try again.")