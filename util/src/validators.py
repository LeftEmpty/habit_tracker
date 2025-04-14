import re

# helper module for validation
""" keep code clean and reduces bloated classes """

#* ******************************************************** user input ********************************************************
def validate_email(email:str) -> bool:
    """Allow basic email format: text@text.text with letters, digits, dots, and hyphens."""
    # @TODO this could be improved to check actual emails but is unecessary/out of scope for this project
    return bool(re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def validate_username(username:str) -> bool:
    """Allow only alphanumeric + underscores, 3–20 chars"""
    return bool(re.fullmatch(r'^\w{3,20}$', username))

def validate_password(password:str) -> bool:
    """Allow only passwords of length between 8 & 16"""
    return 8 <= len(password) <= 16

def contains_empty_input(input:list[str]) -> bool:
    """Returns true if no members of the input list are empty"""
    for i in input:
        if i is "":
            return True
    return False

def contains_naughty_stuff(*args: str) -> bool:
    """funny 'easter egg' function (doesn't serve any 'real' purpose)"""
    funny_checks = [
        "DROP TABLE", "SELECT * FROM", "WHERE 1=1", "--", ";",
        "xp_cmdshell", "UNION", "' OR '1'='1", "exec(",
        "insert into", "delete from", "admin", "root",
    ]

    for arg in args:
        for check in funny_checks:
            if check.lower() in arg.lower():
                return True

    return False