from typing import List, Callable

#@TODO ideally there should be different logging verbosities so that logging doesn't get displayed in the CLI

class InputOption:
    """Input option data class - class used to package an option into a usable format when asking for user input
    @param 'name':
    @param 'key': number pressed to select the option
    @param function_to_call: Reference to the function to execute on callback
    """
    # @TODO - could improve to support any key input, not just numbers, but will be enough for MVP CLI

    # gets set to True if initalized successfully
    is_valid = False
        
    def __init__(self, key:int, name:str, function_to_call:Callable[[], None])->None:
        self.key = key
        self.name = name
        self.function_to_call = function_to_call
        # check if the input is valid and set is_valid
        if (name == "" or (key == 0 or key > 9)or not callable(function_to_call)):
            print("@WARNING: UserInputOption instantiated with invalid data.")
            self.is_valid = False

    def ouput_option(self)->None:
        """display this option in CLI"""
        if (not self.is_valid): return
        print(f"{self.key}: {self.name}")

    # @TODO this may be better in the function_to_call
    def output_feedback(self)->None:
        """display user feedback, if UserInputOption is valid"""
        if (not self.is_valid): return
        print(f"You have selected option: {self.key} - {self.name}")
    
    def callback(self)->None:
        """call the function that is referenced to this option, if UserInputOption is valid"""
        if (not self.is_valid): return
        # 
        self.function_to_call()
        
def prompt_user_input(options:List[InputOption])->bool:
    """ Prints the different options, asks for input and calls the respective functionality of selelected option
    @param 'options': array of options to select, a  
    Returns:
        bool: returns wheter option was successfully selected
    """
    while True:
        # Display the options
        print("\nOptions:")
        print("Press the respective key to choose an option.")
        for option in options:
            option.output_option
            
        
        # Get user input
        choice = input("Enter your choice: ").strip()

        # Handle user input
    
    return False

def prompt_panel()->None:
    """Prompt - which panel to open"""

    # Make options
    List [InputOption] = [
        InputOption(1, "Modify a Habit", open_panel_modify_habit),
        InputOption(1, "Open Dashboard Panel", open_panel_dashboard),
        InputOption(1, "Open Statistics Panel", open_panel_statistics),
    ]
    
    # Display prompt
    
    
def open_panel_login()->bool:
    """ Opens the login panel, i.e. prints out the necessary CLI stuff,
    should not be called intentionally from user. show this if user is logged out
    @return 'bool': True on success
    """
    
    # @TODO - type check input, very important
    
    print(f"__HABIT TRACKER__")
    print(f"\nEnter username: ")
    choice = input("").strip()
    print(f"\nEnter password: ")
    choice = input("").strip()
    
    return True

def evaluate_login(username:str, password:str)->bool:
    # @TODO query db user table for match with hashed data
    return True

def open_panel_modify_habit()->bool:
    """ Opens the habit modification panel, i.e. prints out the necessary CLI stuff 
    @return 'bool': True on success
    """
    
    return True

def open_panel_dashboard()->bool:
    """ Opens the dashboard panel, i.e. prints out the necessary CLI stuff 
    dashboard contains a list of habits that can / should be completed on the given day
    @return 'bool': True on success
    """
        
    return True

def open_panel_statistics()->bool:
    """ Opens the statistics panel, i.e. prints out the necessary CLI stuff 
    @return 'bool': True on success
    """
    
    return True

