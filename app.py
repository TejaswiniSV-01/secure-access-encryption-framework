from getpass import getpass

from security.registration import register_user
from security.authentication import login_user
from security.mfa_enrollment import (
    begin_mfa_enrollment,
    confirm_mfa_enrollment,
)
from security.password_reset import (
    request_password_reset,
    reset_password,
)
from security.file_encryption import (
    encrypt_file,
    decrypt_file,
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
        print("5. Encrypt a File")
        print("6. Decrypt a File")
        print("7. Logout")
        print("8. Exit")
    else:
        print("3. Request Password Reset")
        print("4. Reset Password")
        print("5. Exit")


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


def handle_password_reset_request():
    print("\n--- Password Reset Request ---")

    username = input("Enter your username: ").strip()

    try:
        success, message = request_password_reset(username)
        print(message)
    except Exception:
        print(
            "Unable to send the reset code. "
            "Please try again later."
        )


def handle_password_reset():
    print("\n--- Reset Password ---")

    username = input("Enter your username: ").strip()
    otp = input("Enter the 6-digit verification code: ").strip()

    new_password = getpass("Enter your new password: ")
    confirm_password = getpass("Confirm your new password: ")

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        success, message = reset_password(
            username,
            otp,
            new_password
        )

        print(message)

    except Exception:
        print("Password reset failed. Please try again later.")


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


def handle_file_encryption():
    if not current_user:
        print("Please log in first.")
        return

    print("\n--- File Encryption ---")

    input_path = input("Enter the file path to encrypt: ").strip()
    output_path = input("Enter the encrypted output path: ").strip()

    password = getpass("Enter an encryption password: ")
    confirm_password = getpass("Confirm encryption password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        encrypt_file(
            input_path,
            output_path,
            password
        )

        print("File encrypted successfully!")
        print(f"Encrypted file saved to: {output_path}")

    except (FileNotFoundError, FileExistsError, ValueError, OSError) as error:
        print(f"Encryption failed: {error}")


def handle_file_decryption():
    if not current_user:
        print("Please log in first.")
        return

    print("\n--- File Decryption ---")

    input_path = input("Enter the encrypted file path: ").strip()
    output_path = input("Enter the decrypted output path: ").strip()

    password = getpass("Enter the encryption password: ")

    try:
        decrypt_file(
            input_path,
            output_path,
            password
        )

        print("File decrypted successfully!")
        print(f"Decrypted file saved to: {output_path}")

    except (FileNotFoundError, FileExistsError, ValueError, OSError) as error:
        print(f"Decryption failed: {error}")


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

        elif choice == "5" and current_user:
            handle_file_encryption()

        elif choice == "6" and current_user:
            handle_file_decryption()

        elif choice == "7" and current_user:
            print(f"Goodbye, {current_user}!")
            current_user = None

        elif choice == "8" and current_user:
            print("Exiting Secure Access Framework.")
            current_user = None
            break

        elif choice == "3" and not current_user:
            handle_password_reset_request()

        elif choice == "4" and not current_user:
            handle_password_reset()

        elif choice == "5" and not current_user:
            print("Exiting Secure Access Framework.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        current_user = None
        print("\nApplication closed safely.")
