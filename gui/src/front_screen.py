import tkinter as tk
from tkinter import ttk
from enum import Enum

from gui.util.gui_enums import InputResponse
from gui.src.screen import ScreenBase
import obj.util.request_handler as request

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.src.gui import GUI


class FrontScreenState(Enum):
    """Enum used to determine if frontscreen is in login or register state"""
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"


class FrontScreen(ScreenBase):
    def __init__(self, root:ttk.Frame, gui:"GUI"):
        """"""
        self.cur_state = None
        super().__init__(root, gui)

    def setup_screen(self) -> None:
        """Inherited setup screen function.
        Builds UI of the front screen in this case.
        Also inits screen state to the LOGIN state."""
        super().setup_screen()

        self.update_screen_title("LOGIN")

        self.email_label = ttk.Label(self, text="Email", anchor="w")
        self.email_label.grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=1, column=1, columnspan=2)

        self.username_label = ttk.Label(self, text="Username", anchor="w")
        self.username_label.grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=2, column=1, columnspan=2)

        self.password_label = ttk.Label(self, text="Password", anchor="w")
        self.password_label.grid(row=3, column=0, padx=8, pady=8, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, columnspan=2)

        self.password2_label = ttk.Label(self, text="Confirm Password", anchor="w")
        self.password2_label.grid(row=4, column=0, padx=8, pady=8, sticky="w")
        self.password2_entry = ttk.Entry(self, show="*")
        self.password2_entry.grid(row=4, column=1, columnspan=2)

        self.login_button = ttk.Button(self, text="Login", command=self._login_user)
        self.login_button.grid(row=5, column=0, padx=16, pady=18, sticky="w")

        self.register_button = ttk.Button(self, text="Register", command=self._register_user)
        self.register_button.grid(row=5, column=2, padx=8, pady=18, sticky="e")

        # Updatee Layout to reflect current panel state (init LOGIN)
        self.update_screen_state(FrontScreenState.LOGIN)

    def on_open_screen_event(self) -> None:
        pass

    def _login_user(self) -> None:
        if self.update_screen_state(FrontScreenState.LOGIN):return
        # get input
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())
        # try login, with feedback
        login_response:InputResponse = request.try_login_user(try_usr, try_pw, self.owning_gui)
        self.owning_gui.give_input_feedback(login_response)
        # open home screen on success
        if login_response == InputResponse.SUCCESS:
            self.owning_gui.open_screen_home()

    def _register_user(self) -> None:
        if self.update_screen_state(FrontScreenState.REGISTER): return
        # get input
        try_email:str = str(self.email_entry.get())
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())
        try_pw2:str = str(self.password2_entry.get())
        register_response:InputResponse = request.try_register_user(try_email, try_usr, try_pw, try_pw2)
        self.owning_gui.give_input_feedback(register_response)

    #* **************************************** State functionality ****************************************
    def update_screen_state(self, to_state:FrontScreenState) -> bool:
        """Updates content on FrontScreen and sets state, only if necessary

        Args:
            to_state (FrontScreenState): new state that screen should update to

        Returns:
            bool: returns False if cur_state is the same as to_state, else True
        """
        if self.cur_state == to_state:
            return False
        self.cur_state = to_state

        # adjust layout
        self.update_screen_title(to_state.value)
        if to_state == FrontScreenState.LOGIN:
            # Layout
            self.email_label.grid_remove()
            self.email_entry.grid_remove()
            self.password2_label.grid_remove()
            self.password2_entry.grid_remove()
        elif to_state == FrontScreenState.REGISTER:
            # Layout
            self.email_label.grid()
            self.email_entry.grid()
            self.password2_label.grid()
            self.password2_entry.grid()

        # remove fail feedback when changing screens
        self.owning_gui.close_notification_bar
        return True