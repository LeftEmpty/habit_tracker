import tkinter as tk
from tkinter import ttk
from abc import abstractmethod
from frontend.src.frame import FrameBase

class PanelBase(FrameBase):
    def __init__(self, root_gui, root_notebook:ttk.Notebook)->None:
        """Abstract base class for all Panels used in this project."""
        # Make this object a Frame attached to notebook (root_ref is the notebook)
        super().__init__(root_gui)
        self.owning_notebook = root_notebook
        self.setup_panel()

    @abstractmethod
    def setup_panel(self, panel_name:str = "Panel")->None:
        """add self to root_ref notebook, overwrite for panel specific functionality"""
        self.owning_notebook.add(self, text=panel_name)