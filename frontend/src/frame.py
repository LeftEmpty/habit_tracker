import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class FrameBase(ttk.Frame, ABC):
    """ FrameBase (Tkinter Frame)
    Frame base (abstract) class used for all 'main frames' in the project
    Main frames are subcategorized into panels & screen 
    
    Screens are completely seperate from each other, e.g.: login/main screens
        Panels are somewhat connected in that they are contained in the same notebook on the main screen
    """
    def __init__(self)->None:
        # Make this object a Frame
        super().__init__()
        
    def __init__(self, root_reference:ttk.Notebook)->None:
        # Make this object a Frame
        super().__init__(root_reference)
        
    @abstractmethod
    def setup_frame()->None:
        """override this function in child class"""
        pass