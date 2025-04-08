import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

from frontend.src.frame import FrameBase

class PanelBase(FrameBase):
    """Abstract base class for all Panels used in this project."""
    
    def __init__(self, root_reference:ttk.Notebook)->None:
        # Make this object a Frame attached to notebook (root_ref is the notebook)
        super().__init__(root_reference)  
        self.root_ref = root_reference
    
    @abstractmethod
    def setup_panel()->None:
        pass