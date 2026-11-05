import unittest
from unittest.mock import patch

import web.app as web_app


class TestWebApplication(unittest.TestCase):

    def setUp(self):
        # Enable Flask testing mode.
        web_app.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
        )

        # Create a test browser client.
        self.client = web_app.app.test_client()

    def tearDown(self):
        # Clear the test session.
        with self.client.session_transaction() as session:
            session.clear()

    def test_homepage_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Secure Access",
            response.data,
        )

    def test_registration_page_loads(self):
        response = self.client.get("/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    @patch(
        "web.app.register_user",
        return_value=(True, "Registration successful."),
    )
    def test_successful_registration(self, mock_register):
        response = self.client.post(
            "/register",
            data={
                "username": "testuser",
                "email": "",
                "password": "StrongPassword123!",
                "confirm_password": "StrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        mock_register.assert_called_once_with(
            "testuser",
            "StrongPassword123!",
            None,
        )

    @patch("web.app.register_user")
    def test_registration_password_mismatch(self, mock_register):
        response = self.client.post(
            "/register",
            data={
                "username": "testuser",
                "email": "",
                "password": "Password123!",
                "confirm_password": "DifferentPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        mock_register.assert_not_called()

        response = self.client.get(response.location)
        self.assertIn(b"Passwords do not match.", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    @patch(
        "web.app.login_user",
        return_value=(True, "Login successful."),
    )
    def test_successful_login(self, mock_login):
        response = self.client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "StrongPassword123!",
                "mfa_code": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "/dashboard",
        )

        mock_login.assert_called_once_with(
            "testuser",
            "StrongPassword123!",
            None,
        )

        with self.client.session_transaction() as session:
            self.assertEqual(session["username"], "testuser")

    @patch(
        "web.app.login_user",
        return_value=(False, "Invalid username or password."),
    )
    def test_failed_login(self, mock_login):
        response = self.client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "WrongPassword123!",
                "mfa_code": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/login")

        with self.client.session_transaction() as session:
            self.assertNotIn("username", session)

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/login")

    def test_authenticated_user_can_access_dashboard(self):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome, testuser!", response.data)

    def test_logout_clears_session(self):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.post("/logout")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")

        with self.client.session_transaction() as session:
            self.assertNotIn("username", session)

    def test_csrf_protection_rejects_missing_token(self):
        web_app.app.config["WTF_CSRF_ENABLED"] = True

        response = self.client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "StrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_mfa_setup_requires_login(self):
        response = self.client.get("/mfa/setup")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/login")

    def test_mfa_confirm_requires_login(self):
        response = self.client.post(
            "/mfa/confirm",
            data={
                "password": "StrongPassword123!",
                "mfa_code": "123456",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/login")

    def test_authenticated_user_can_access_mfa_setup(self):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.get("/mfa/setup")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Set Up MFA", response.data)

    @patch(
        "web.app.begin_mfa_enrollment",
        return_value=(
            True,
            "MFA enrollment started.",
            "otpauth://totp/test",
        ),
    )
    def test_successful_mfa_setup(self, mock_begin):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.post(
            "/mfa/setup",
            data={"password": "StrongPassword123!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"otpauth://totp/test", response.data)
        mock_begin.assert_called_once_with(
            "testuser",
            "StrongPassword123!",
        )

    @patch(
        "web.app.confirm_mfa_enrollment",
        return_value=(True, "MFA enabled successfully."),
    )
    def test_successful_mfa_confirmation(self, mock_confirm):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.post(
            "/mfa/confirm",
            data={
                "password": "StrongPassword123!",
                "mfa_code": "123456",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/dashboard")
        mock_confirm.assert_called_once_with(
            "testuser",
            "StrongPassword123!",
            "123456",
        )

    @patch(
        "web.app.confirm_mfa_enrollment",
        return_value=(False, "Invalid MFA code."),
    )
    def test_failed_mfa_confirmation(self, mock_confirm):
        with self.client.session_transaction() as session:
            session["username"] = "testuser"

        response = self.client.post(
            "/mfa/confirm",
            data={
                "password": "StrongPassword123!",
                "mfa_code": "000000",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/mfa/setup")
        mock_confirm.assert_called_once()

if __name__ == "__main__":
    unittest.main()
