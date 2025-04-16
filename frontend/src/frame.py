import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

class FrameBase(tk.Frame, ABC):
    """ FrameBase (Tkinter Frame)
    Frame base (abstract) class used for all 'main frames' in the project
    Main frames are subcategorized into panels & screen

    Screens are completely seperate from each other, e.g.: login/main screens
    Panels are somewhat connected in that they are contained in the same notebook on the main screen
    """
    def __init__(self, root_gui) -> None:
        # Make this object a Frame
        super().__init__(root_gui.root)
        self.root_gui = root_gui
