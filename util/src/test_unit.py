import os

# globals
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # clear console depending on os
