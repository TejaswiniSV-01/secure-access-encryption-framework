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
        result = register_user("testuser", "StrongPassword123")

        self.assertEqual(
            result,
            (True, "Registration successful.")
        )

    @patch("security.registration.is_valid_username", return_value=True)
    @patch("security.registration.hash_password", return_value="hashed_password")
    @patch("security.registration.add_user", return_value=False)
    def test_duplicate_user_returns_failure(
        self, mock_add_user, mock_hash_password, mock_username
    ):
        result = register_user("testuser", "StrongPassword123")

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
        result = register_user("testuser", "StrongPassword123")

        self.assertEqual(
            result,
            (False, "Registration could not be completed. Please try again later.")
        )


if __name__ == "__main__":
    unittest.main()

