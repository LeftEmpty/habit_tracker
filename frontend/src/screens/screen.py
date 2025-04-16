from frontend.src.frame import FrameBase
from abc import abstractmethod

class ScreenBase(FrameBase):
    def __init__(self, root_gui) -> None:
        """Screen base class, inherited from Frame base, used to template all screens in this project"""
        super().__init__(root_gui)
        self.setup_screen()


    @abstractmethod
    def setup_screen(self) -> None:
        """Sets up the screen, super base class contians common setup functionality
        Screens should overwrite to implement specifics, such as creating widgets / init layout, then call"""
        self.config(bg="#000")
