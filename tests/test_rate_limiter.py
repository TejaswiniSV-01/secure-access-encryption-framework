
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from security.rate_limiter import (
    MAX_FAILED_ATTEMPTS,
    LOCKOUT_SECONDS,
    is_locked,
    record_failed_attempt,
    reset_failed_attempts,
    cleanup_old_attempts,
)


class TestRateLimiter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.database_path = Path(self.temp_dir.name) / "test.db"

        self.database_patcher = patch(
            "security.database.DATABASE_PATH",
            self.database_path,
        )
        self.database_patcher.start()
        self.addCleanup(self.database_patcher.stop)

        from security.database import create_database
        create_database()

    def test_account_initially_not_locked(self):
        self.assertFalse(is_locked("testuser", now=1000))

    def test_different_users_have_separate_counters(self):
        record_failed_attempt("user1", now=1000)
        record_failed_attempt("user2", now=1000)

        self.assertFalse(is_locked("user1", now=1000))
        self.assertFalse(is_locked("user2", now=1000))

    def test_lockout_starts_after_fifth_failure(self):
        for _ in range(MAX_FAILED_ATTEMPTS):
            record_failed_attempt("testuser", now=1000)

        self.assertTrue(is_locked("testuser", now=1000))

    def test_locked_attempt_does_not_increase_counter(self):
        for _ in range(MAX_FAILED_ATTEMPTS):
            record_failed_attempt("testuser", now=1000)

        record_failed_attempt("testuser", now=1001)

        with closing(sqlite3.connect(self.database_path)) as connection:
            result = connection.execute(
                "SELECT failed_attempts FROM login_attempts "
                "WHERE username = ?",
                ("testuser",),
            ).fetchone()

        self.assertEqual(result[0], MAX_FAILED_ATTEMPTS)

    def test_lockout_expires_after_five_minutes(self):
        for _ in range(MAX_FAILED_ATTEMPTS):
            record_failed_attempt("testuser", now=1000)

        self.assertFalse(
            is_locked("testuser", now=1000 + LOCKOUT_SECONDS + 1)
        )

    def test_reset_clears_failed_attempts(self):
        record_failed_attempt("testuser", now=1000)

        self.assertTrue(reset_failed_attempts("testuser"))

        with closing(sqlite3.connect(self.database_path)) as connection:
            result = connection.execute(
                "SELECT username FROM login_attempts WHERE username = ?",
                ("testuser",),
            ).fetchone()

        self.assertIsNone(result)
        self.assertFalse(is_locked("testuser", now=1000))

    def test_failed_attempt_counter_resets_after_lockout_expires(self):
        for _ in range(MAX_FAILED_ATTEMPTS):
            record_failed_attempt("testuser", now=1000)

        record_failed_attempt(
            "testuser",
            now=1000 + LOCKOUT_SECONDS + 1,
        )

        with closing(sqlite3.connect(self.database_path)) as connection:
            result = connection.execute(
                "SELECT failed_attempts FROM login_attempts "
                "WHERE username = ?",
                ("testuser",),
            ).fetchone()

        self.assertEqual(result[0], 1)

    def test_updated_at_changes_when_failure_is_recorded(self):
        record_failed_attempt("testuser", now=2000)

        with closing(sqlite3.connect(self.database_path)) as connection:
            result = connection.execute(
                "SELECT updated_at FROM login_attempts "
                "WHERE username = ?",
                ("testuser",),
            ).fetchone()

        self.assertEqual(result[0], 2000)

    def test_cleanup_removes_old_inactive_records(self):
        record_failed_attempt("olduser", now=1000)

        deleted = cleanup_old_attempts(
            max_age_seconds=50,
            now=1100,
        )

        self.assertEqual(deleted, 1)

        with closing(sqlite3.connect(self.database_path)) as connection:
            result = connection.execute(
                "SELECT username FROM login_attempts "
                "WHERE username = ?",
                ("olduser",),
            ).fetchone()

        self.assertIsNone(result)

    def test_cleanup_preserves_active_lockouts(self):
        for _ in range(MAX_FAILED_ATTEMPTS):
            record_failed_attempt("lockeduser", now=1000)

        deleted = cleanup_old_attempts(
            max_age_seconds=50,
            now=1100,
        )

        self.assertEqual(deleted, 0)
        self.assertTrue(is_locked("lockeduser", now=1100))

    def test_empty_username_is_rejected(self):
        with self.assertRaises(ValueError):
            is_locked("")

        with self.assertRaises(ValueError):
            record_failed_attempt("")

        with self.assertRaises(ValueError):
            reset_failed_attempts("")

    def test_non_string_username_is_rejected(self):
        with self.assertRaises(ValueError):
            is_locked(None)

        with self.assertRaises(ValueError):
            record_failed_attempt(None)

        with self.assertRaises(ValueError):
            reset_failed_attempts(None)

    def test_whitespace_username_is_rejected(self):
        with self.assertRaises(ValueError):
            is_locked("   ")

        with self.assertRaises(ValueError):
            record_failed_attempt("   ")

        with self.assertRaises(ValueError):
            reset_failed_attempts("   ")


if __name__ == "__main__":
    unittest.main()

