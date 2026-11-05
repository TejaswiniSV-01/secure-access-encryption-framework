import unittest

from app import has_reached_demo_threshold
from security.validation import is_valid_username
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import app

class TestProjectHelpers(unittest.TestCase):

    def test_threshold_below_limit(self):
        self.assertFalse(has_reached_demo_threshold(3))

    def test_threshold_at_limit(self):
        self.assertTrue(has_reached_demo_threshold(5))

    def test_threshold_custom_limit(self):
        self.assertFalse(
            has_reached_demo_threshold(7, threshold=10)
        )

    def test_valid_username(self):
        self.assertTrue(is_valid_username("tejaswini"))

    def test_valid_username_with_allowed_symbols(self):
        self.assertTrue(is_valid_username("tejaswini_25"))

    def test_empty_username(self):
        self.assertFalse(is_valid_username(""))

    def test_whitespace_username(self):
        self.assertFalse(is_valid_username("   "))

    def test_username_too_short(self):
        self.assertFalse(is_valid_username("ab"))

    def test_username_too_long(self):
        self.assertFalse(is_valid_username("a" * 33))

    def test_username_with_invalid_characters(self):
        self.assertFalse(is_valid_username("tejaswini!!!"))

    def test_username_starting_with_symbol(self):
        self.assertFalse(is_valid_username("_tejaswini"))

    def test_username_with_surrounding_spaces(self):
        self.assertFalse(is_valid_username(" tejaswini "))

    def test_non_string_username(self):
        self.assertFalse(is_valid_username(123))

class TestApplicationSession(unittest.TestCase):

    def setUp(self):
        app.current_user = None

    def tearDown(self):
        app.current_user = None

    def test_successful_login_creates_session(self):
        with patch("builtins.input", side_effect=[
            "Vasudeva", ""
        ]), patch(
            "app.getpass", return_value="example-password"
        ), patch(
            "app.login_user",
            return_value=(True, "Login successful.")
        ):
            app.handle_login()

        self.assertEqual(app.current_user, "Vasudeva")

    def test_failed_login_does_not_create_session(self):
        with patch("builtins.input", side_effect=[
            "Vasudeva", ""
        ]), patch(
            "app.getpass", return_value="wrong-password"
        ), patch(
            "app.login_user",
            return_value=(False, "Invalid username or password.")
        ):
            app.handle_login()

        self.assertIsNone(app.current_user)

    def test_logout_clears_session(self):
        app.current_user = "Vasudeva"

        with patch(
            "builtins.input",
            side_effect=["7", "5"]
        ), redirect_stdout(StringIO()):
            app.main()

        self.assertIsNone(app.current_user)

if __name__ == "__main__":
    unittest.main()
