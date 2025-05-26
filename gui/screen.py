import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI


class ScreenBase(ttk.Frame, ABC):
    def __init__(self, root:ttk.Frame, gui:"GUI"):
        """Screen base class, inherited from Frame base, used to template all screens in this project"""
        super().__init__(root)
        self.owning_gui = gui
        self.root = root

        self.setup_screen()

    @abstractmethod
    def setup_screen(self) -> None:
        """Sets up the screen, super base class contains common setup functionality
        Screens should overwrite to implement specifics, such as creating widgets / init layout, then call"""
        # Default setup for all screens
        self.config(style="ContentArea.TFrame")
        self.title_label = ttk.Label(self, text="", anchor="w", font=("TkDefaultFont", 26, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=8, padx=8, sticky="w")

        # Debugging
        print(f"Log: Setting up " + self.__class__.__name__)
        # self.config(borderwidth=2, relief="solid")

    @abstractmethod
    def on_open_screen_event(self) -> None:
        """Can be used to fire logic that is requried for the screen is called in base GUI when screen is opened (via e.g. sidebar).
        Importantly this function is not called during construction, this means the user is likely set in this function."""
        pass

    def update_screen_title(self, new_title:str) -> None:
        self.title_label.config(text=new_title)