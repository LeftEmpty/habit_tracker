

def validate_input(input:str) -> bool:
    """checks input for validity, no special characters allowed"""
    special_characters = " \"!@#$%^&*()-+?_=,<>/"
    return any(c in special_characters for c in input)