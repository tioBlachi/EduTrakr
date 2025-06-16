"""
This file will contain utility fucntions that are now

"""

import re

def is_valid_email(email):
    """
    Validate an email using regex
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(pattern, email) is not None