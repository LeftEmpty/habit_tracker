from frontend.src.frame import FrameBase
from abc import abstractmethod

class ScreenBase(FrameBase):
    """Screen base class, inherited from Frame base, used to template all screens in this project"""
    def __init__(self, root_reference) -> None: # type: ignore (tk.Tk)
        super().__init__(root_reference) # type: ignore (tk.Tk)
        pass

    @abstractmethod
    def setup_screen(self)->None:
        pass

    def setup_frame(self)->None:
        self.setup_screen()
        pass
