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
        


