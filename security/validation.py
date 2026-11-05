def is_valid_username(username):
    if not isinstance(username, str):
        return False

    if not 3 <= len(username) <= 32:
        return False

    letters_and_digits = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )

    allowed_characters = letters_and_digits + "_.-"

    if username[0] not in letters_and_digits:
        return False

    return all(
        character in allowed_characters
        for character in username
    )

