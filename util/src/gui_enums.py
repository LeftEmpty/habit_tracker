from enum import Enum


class PanelState(Enum):
    LOGIN = "Login"
    REGISTER = "Register"

class InputResponse(Enum):
    DEFAULT = "Couldn't process that action."

    SUCCESS = "Success."

    EMPTY_FIELDS = "Please fill in all required fields."
    INVALID_EMAIL = "Invalid e-mail."
    INVALID_USR = "Invalid username."
    INVALID_PW = "Invalid password."
    MISMATCH_PW = "The passwords don't match"
    EMAIL_EXISTS = "Email already in use."
    USR_EXISTS = "Username taken."
    NAUGHTY = "Dont do that, you know what you did =)"
