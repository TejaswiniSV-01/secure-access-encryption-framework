
import sqlite3
import unittest
from unittest.mock import patch

from security.registration import register_user


class TestRegistration(unittest.TestCase):

    @patch("security.registration.is_valid_username", return_value=True)
    @patch("security.registration.hash_password", return_value="hashed_password")
    @patch("security.registration.add_user", return_value=True)
    def test_registration_succeeds(
        self, mock_add_user, mock_hash_password, mock_username
    ):
        result = register_user("testuser", "StrongPassword123!")

        self.assertEqual(result, (True, "Registration successful."))

    @patch("security.registration.is_valid_username", return_value=True)
    @patch("security.registration.hash_password", return_value="hashed_password")
    @patch("security.registration.add_user", return_value=False)
    def test_duplicate_user_returns_failure(
        self, mock_add_user, mock_hash_password, mock_username
    ):
        result = register_user("testuser", "StrongPassword123!")

        self.assertEqual(
            result,
            (False, "Username or email already exists.")
        )

    @patch("security.registration.is_valid_username", return_value=True)
    @patch("security.registration.hash_password", return_value="hashed_password")
    @patch(
        "security.registration.add_user",
        side_effect=sqlite3.OperationalError("Database unavailable")
    )
    def test_database_error_returns_controlled_failure(
        self, mock_add_user, mock_hash_password, mock_username
    ):
        result = register_user("testuser", "StrongPassword123!")

        self.assertEqual(
            result,
            (False, "Registration could not be completed. Please try again later.")
        )

    def test_weak_password_is_rejected(self):
        weak_passwords = [
            "short1!",
            "alllowercase123!",
            "ALLUPPERCASE123!",
            "NoNumbersHere!!",
            "NoSpecialCharacter123"
        ]

        for password in weak_passwords:
            with self.subTest(password=password):
                success, message = register_user("testuser", password)
                self.assertFalse(success)
                self.assertIn("Password must contain", message)

    def test_password_with_all_requirements_is_accepted(self):
        with patch("security.registration.add_user", return_value=True):
            success, message = register_user(
                "testuser", "StrongPassword123!"
            )

        self.assertTrue(success)
        self.assertEqual(message, "Registration successful.")


if __name__ == "__main__":
    unittest.main()
