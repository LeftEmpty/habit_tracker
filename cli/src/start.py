import os
from sqlite_rx.client import SQLiteClient # type: ignore
from .login_handler import create_user, login_user
#globals
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def user_input_loop(sql_client: SQLiteClient) -> None:

    login_user(sql_client)

    #Habit management
    while True:

        # Display a menu or prompt
        print("\nOptions:")
        print("1. Create Habit")
        print("2. Logout")
        print("3. Exit")
        
        # Get user input
        choice = input("Enter your choice: ").strip()
        
        # Handle user input
        if choice == "1":
            print("You selected Option 1.")
            create_habit(
                sql_client=sql_client,  # Replace with actual SQLite client instance
                habit_name="Exercise",
                habit_description="Daily workout",
                frequency=1,
                timeframe="daily"
            )
        elif choice == "2":
            pass

        elif choice == "3":
            print("Exiting...")
            break  # Exit the loop
        else:
            print("Invalid choice. Please try again.")


def start() -> None:
    client = SQLiteClient(connect_address="tcp://127.0.0.1:5000")
    with client:

        # Perform operations with the client
        print("Connected to SQLite server.")
        user_input_loop(client)
        # Example: Execute a query
        # result = client.execute("SELECT * FROM your_table")
        # print(result)

    
