from typing import List
from frontend.src.cli.input_option import InputOption

# @DEPRECATED - legacy code, abandonded when changed to gui

def prompt_user(options:List[InputOption])->bool:
    """Prints the different options, asks for input and calls the respective functionality of selelected option
    @param 'options': array of options to select, a
    Returns:
        bool: returns wheter option was successfully selected
    """
    while True:
        # Display the options (cancel if we find an invalid option in list)
        print("\nOptions:")
        print("Press the respective key to choose an option.")
        for option in options:
            if (not option.output_option()): return
        # Get user input
        choice = input("Enter your choice: ").strip()

        # Handle user input
        if choice.isdigit():
            choice_int = int(choice)
            if (0 <= choice_int <= 9):
                for i, option in enumerate[options]:
                    if (i == option.key):
                        option.callback()
                        break
            else:
                print("Please choose a number that correlates to an option.")
        else:
            print("Invalid input. Please enter a number (correlating to an option).")
    return False

def debug_prompt_panels()->None:
    """Prompt - which panel to open"""

    # Make options
    Options: List[InputOption] = [
    InputOption(1, "Modify a Habit", open_panel_modify_habit),
    InputOption(2, "Open Dashboard Panel", open_panel_dashboard),
    InputOption(3, "Open Statistics Panel", open_panel_statistics),
    ]

    # Prompt user
    prompt_user(Options)


def open_panel_login()->bool:
    """ Opens the login panel, i.e. prints out the necessary CLI stuff,
    should not be called intentionally from user. show this if user is logged out
    @return 'bool': True on success
    """

    # @TODO - type check input, very important

    return True

def evaluate_login(username:str, password:str)->bool:
    # @TODO query db user table for match with hashed data
    return True

def open_panel_modify_habit()->bool:
    """ Opens the habit modification panel, i.e. prints out the necessary CLI stuff 
    @return 'bool': True on success
    """

    print(f"opening habit modification")

    return True

def open_panel_dashboard()->bool:
    """ Opens the dashboard panel, i.e. prints out the necessary CLI stuff 
    dashboard contains a list of habits that can / should be completed on the given day
    @return 'bool': True on success
    """

    print(f"opening dashboard")

    return True

def open_panel_statistics()->bool:
    """ Opens the statistics panel, i.e. prints out the necessary CLI stuff 
    @return 'bool': True on success
    """

    print(f"opening statistics")

    return True
