"""
This file will contain utility fucntions that are not
file specific

"""

import re
from faker import Faker
from datetime import timedelta
import hashlib


fake = Faker()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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

def is_valid_password(password: str) -> bool:
    """
    Returns True if the password is at least 8 characters long,
    contains at least one uppercase letter, one lowercase letter,
    one digit, and one special character.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.fullmatch(pattern, password))