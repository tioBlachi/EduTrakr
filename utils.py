"""
This file will contain utility fucntions that are not
file specific

"""

import re

def is_valid_email(email: str) -> bool:
    """
    Validate an email using regex
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(pattern, email) is not None

def is_valid_name(name: str) -> bool:
    """
    Returns True if the name contains only letters and spaces,
    and starts with a letter.
    """
    pattern = r"^[A-Za-z][A-Za-z\s'-]*$"
    return bool(re.fullmatch(pattern, name.strip()))

