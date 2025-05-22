from enum import Enum


class InputResponse(Enum):
    """Response used to determine result of input action.
    Is usually displayed via notification bar via value string."""
    NONE = ""
    DEFAULT = "Couldn't process that action."

    SUCCESS = "Success."

    # Login / Register
    EMPTY_FIELDS = "Please fill in all required fields."
    INVALID_EMAIL = "Invalid e-mail."
    INVALID_USR = "Invalid username."
    INVALID_PW = "Invalid password."
    MISMATCH_PW = "The passwords don't match"
    EMAIL_EXISTS = "Email already in use."
    USR_EXISTS = "Username taken."
    USR_NOTFOUND = "Wrong login information."
    NAUGHTY = "Dont do that, you know what you did =)"


class GUITheme(Enum):
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"


class HabitListMode(Enum):
    SUB = "sub"
    DATA = "data"

class HabitQueryCondition(Enum):
    """Condition that can be passed when habits are querried to adjust result."""
    NONE = "NONE",
    ALL = "ALL"
    RELEVANT_TODAY = "RELEVANT TODAY" # revelant for the day
    DUE = "DUE",
    COMPLETED = "COMPLETED"
