
from getpass import getpass

from security.registration import register_user
from security.authentication import login_user
from security.validation import is_valid_username
from security.mfa_enrollment import (
    begin_mfa_enrollment,
    confirm_mfa_enrollment,
)

current_user = None


def has_reached_demo_threshold(attempts, threshold=5):
    return attempts >= threshold


def show_menu():
    print("\n================================")
    print(" Secure Access & Encryption ")
    print("================================")
    print("1. Register")
    print("2. Login")

    if current_user:
        print("3. Set up MFA")
        print("4. Confirm MFA")
        print("5. Logout")
        print("6. Exit")
    else:
        print("3. Exit")


def handle_registration():
    print("\n--- User Registration ---")

    username = input("Enter username: ")
    password = getpass("Enter password: ")
    email = input("Enter email (optional): ").strip()

    if not email:
        email = None

    success, message = register_user(
        username,
        password,
        email
    )

    print(message)


def handle_login():
    global current_user

    print("\n--- User Login ---")

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    mfa_code = input(
        "Enter MFA code (if enabled, otherwise press Enter): "
    )

    if not mfa_code:
        mfa_code = None

    success, message = login_user(
        username,
        password,
        mfa_code
    )

    print(message)

    if success:
        current_user = username
        print(f"Welcome, {current_user}!")


def handle_mfa_setup():
    if not current_user:
        print("Please log in first.")
        return

    print("\n--- MFA Setup ---")

    password = getpass("Re-enter your account password: ")

    success, message, setup_uri = begin_mfa_enrollment(
        current_user,
        password
    )

    print(message)

    if success:
        print("\nScan this setup URI with your authenticator app:")
        print(setup_uri)
        print("\nNext, choose 'Confirm MFA' and enter your code.")


def handle_mfa_confirmation():
    if not current_user:
        print("Please log in first.")
        return

    print("\n--- MFA Confirmation ---")

    password = getpass("Re-enter your account password: ")
    code = input("Enter the 6-digit authenticator code: ").strip()

    success, message = confirm_mfa_enrollment(
        current_user,
        password,
        code
    )

    print(message)


def main():
    global current_user

    while True:
        show_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_registration()

        elif choice == "2":
            handle_login()

        elif choice == "3" and current_user:
            handle_mfa_setup()

        elif choice == "4" and current_user:
            handle_mfa_confirmation()

        elif choice == "3" and not current_user:
            print("Exiting Secure Access Framework.")
            break

        elif choice == "5" and current_user:
            print(f"Goodbye, {current_user}!")
            current_user = None

        elif choice == "6" and current_user:
            print("Exiting Secure Access Framework.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication closed safely.")
