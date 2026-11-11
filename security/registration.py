
import re
import sqlite3

from security.validation import is_valid_username
from security.database import add_user
from security.passwords import hash_password


def is_valid_email(email):
    if not isinstance(email, str):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(pattern, email) is not None


def is_strong_password(password):
    if not isinstance(password, str) or len(password) < 12:
        return False

    return (
        re.search(r"[A-Z]", password) is not None
        and re.search(r"[a-z]", password) is not None
        and re.search(r"\d", password) is not None
        and re.search(r"[^A-Za-z0-9]", password) is not None
    )


def register_user(username, password, email=None):
    if not is_valid_username(username):
        return False, "Invalid username."

    if not is_strong_password(password):
        return False, (
            "Password must contain at least 12 characters, "
            "including uppercase and lowercase letters, "
            "a number, and a special character."
        )

    if email is not None and not is_valid_email(email):
        return False, "Invalid email address."

    password_hash = hash_password(password)

    try:
        if not add_user(username, password_hash, email):
            return False, "Username or email already exists."

    except sqlite3.Error:
        return False, "Registration could not be completed. Please try again later."

    return True, "Registration successful."
