from sqlite_rx.client import SQLiteClient

def user_input_loop():
    while True:
        # Display a menu or prompt
        print("\nOptions:")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Exit")
        
        # Get user input
        choice = input("Enter your choice: ").strip()
        
        # Handle user input
        if choice == "1":
            print("You selected Option 1.")
            # Add logic for Option 1
        elif choice == "2":
            print("You selected Option 2.")
            # Add logic for Option 2
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
        user_input_loop()
        # Example: Execute a query
        # result = client.execute("SELECT * FROM your_table")
        # print(result)

    
