import tkinter as tk
from frontend.src.screens.screen import ScreenBase
from util.src.validators import validate_input_login, validate_input_register
from util.src.gui_enums import PanelState, InputResponse
from frontend.src.screens.main_screen import MainScreen


class LoginScreen(ScreenBase):
    #* **************************************** overwriting base class functionality ****************************************
    def __init__(self, root_gui) -> None:
        """@TODO docstring for class"""
        self.cur_panel = None
        super().__init__(root_gui)

    def setup_screen(self) -> None:
        super().setup_screen()

        # Widgets
        self.title_label = tk.Label(self, text="LOGIN", bg='#000', fg="#fff", font=("Roboto", 34), anchor="w")
        self.email_label = tk.Label(self, text="Email", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.email_entry = tk.Entry(self)
        self.username_label = tk.Label(self, text="Username", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password2_label = tk.Label(self, text="Confirm Password", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.password2_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_login)
        self.register_button = tk.Button(self, text="Register", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_register)
        self.inputfeedback_label = tk.Label(self, text="", bg='#000', fg="#fff", font=("Roboto", 9, "italic"), anchor="center")

        # Set Layout
        self.title_label.grid(row=0, column=0, columnspan=2, pady=8, padx=8, sticky="w")
        self.email_label.grid(row=1, column=0, padx=8, sticky="w")
        self.email_entry.grid(row=1, column=1, columnspan=2)
        self.username_label.grid(row=2, column=0, padx=8, sticky="w")
        self.username_entry.grid(row=2, column=1, columnspan=2)
        self.password_label.grid(row=3, column=0, padx=8, sticky="w")
        self.password_entry.grid(row=3, column=1, columnspan=2)
        self.password2_label.grid(row=4, column=0, padx=8, sticky="w")
        self.password2_entry.grid(row=4, column=1, columnspan=2)
        self.login_button.grid(row=5, column=0, pady=12)
        self.register_button.grid(row=5, column=2, pady=18)
        self.inputfeedback_label.grid(row=6, column=0, columnspan=3, pady=8)

        # Updatee Layout to reflect current panel state (init LOGIN)
        self.update_screen(PanelState.LOGIN)

        # debug / info
        print("login screen setup completed")


    #* **************************************** login / register functionality ****************************************
    def try_login(self) -> None:
        """Swap panel OR Check input, then pass validated and hashed input to action handler
        On faiklure: give input response feebback"""
        if self.update_screen(PanelState.LOGIN): return

        # get input
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())

        # validate input
        response = validate_input_login(try_usr, try_pw)
        if response != InputResponse.SUCCESS:
            self.give_input_feedback(response)
            return

        # query db via action handler
        print(f"trying login with valid input, usr: {try_usr}, pw: {try_pw}")
        maybe_user = self.root_gui.action_handler_ref.try_login_user(try_usr, try_pw)
        if not maybe_user:
            self.give_input_feedback(InputResponse.USR_NOTFOUND)
            return
        # SUCCESS: verification was good
        else:
            self.give_input_feedback(InputResponse.SUCCESS)
            self.root_gui.on_login(maybe_user)

    def try_register(self) -> None:
        """Swap panel OR Check input, then pass validated and hashed input to action handler
        On failure: give appropriate input response feebback."""
        if self.update_screen(PanelState.REGISTER): return

        # get input
        try_email:str = str(self.email_entry.get())
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())
        try_pw2:str = str(self.password2_entry.get())

        # validate input
        response = validate_input_register(try_email, try_usr, try_pw, try_pw2)
        self.give_input_feedback(response)
        if response != InputResponse.SUCCESS:
            return

        # everything is checked, create new user and send email (email service is out of scope)
        print(f"trying register with valid input, email: {try_email}, usr: {try_usr}, pw: {try_pw}, pw2: {try_pw2}")
        if self.root_gui.action_handler_ref.try_register_user(try_usr, try_email, try_pw):
            self.give_input_feedback(InputResponse.SUCCESS)
        else:
            self.give_input_feedback(InputResponse.DEFAULT)

    #* **************************************** GUI / feedback functionality ****************************************
    def update_screen(self, to_panel:PanelState) -> bool:
        """updates panel on LoginScreen, but only if necessary
        @param to_panel: new panel that screen should update to"""
        if self.cur_panel == to_panel: return False
        self.cur_panel = to_panel

        # adjust layout
        self.title_label.config(text=to_panel.value)
        if to_panel == PanelState.LOGIN:
            # Layout
            self.email_label.grid_remove()
            self.email_entry.grid_remove()
            self.password2_label.grid_remove()
            self.password2_entry.grid_remove()
        elif to_panel == PanelState.REGISTER:
            # Layout
            self.email_label.grid()
            self.email_entry.grid()
            self.password2_label.grid()
            self.password2_entry.grid()

        # remove fail feedback when changing screens
        self.inputfeedback_label.config(text="")

        return True

    def give_input_feedback(self, response:InputResponse) -> None:
        """Sets the text of 'inputfeedback_label' element according to the received response.
        That text/label is initially empty (and thus hidden)

        Args:
            response (InputResponse): response enum, value of Enum will determine displayedtext
        """
        self.inputfeedback_label.config(text=response.value)
        if response == InputResponse.SUCCESS:
            self.inputfeedback_label.config(fg="green")
        else:
            self.inputfeedback_label.config(fg="red")
            # @TODO could add some fancy stuff here, e.g. 'switch statement' that marks relevant widgets red, etc.
        print(f"input response: {response.value}")
