from frontend.src.panels.panel import PanelBase
from tkinter import ttk

class HabitsPanel(PanelBase):
    def __init__(self, root_gui, root_notebook:ttk.Notebook) -> None:
        super().__init__(root_gui, root_notebook)

    def setup_panel(self, panel_name:str = "Panel") -> None:
        super().setup_panel("Habits")

