import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from security.database import create_database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.database_path = Path(self.temp_dir.name) / "test_users.db"

        self.database_patch = patch(
            "security.database.DATABASE_PATH",
            self.database_path,
        )
        self.database_patch.start()
        self.addCleanup(self.database_patch.stop)

    def test_database_creates_required_tables(self):
        create_database()

        with closing(sqlite3.connect(self.database_path)) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type = 'table'"
                ).fetchall()
            }

        self.assertIn("users", tables)
        self.assertIn("login_attempts", tables)
        self.assertIn("password_reset_tokens", tables)

    def test_database_creation_is_repeatable(self):
        create_database()
        create_database()

        self.assertTrue(self.database_path.exists())

    def test_existing_login_attempts_table_is_preserved(self):
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                connection.execute("""
                    CREATE TABLE login_attempts (
                        username TEXT PRIMARY KEY,
                        failed_attempts INTEGER NOT NULL DEFAULT 0,
                        locked_until REAL NOT NULL DEFAULT 0
                    )
                """)
                connection.execute(
                    "INSERT INTO login_attempts "
                    "(username, failed_attempts, locked_until) "
                    "VALUES (?, ?, ?)",
                    ("testuser", 3, 0),
                )

        create_database()

        with closing(sqlite3.connect(self.database_path)) as connection:
            row = connection.execute(
                "SELECT failed_attempts FROM login_attempts "
                "WHERE username = ?",
                ("testuser",),
            ).fetchone()

        self.assertEqual(row[0], 3)

    def test_existing_login_attempts_table_gets_updated_at_column(self):
        with closing(sqlite3.connect(self.database_path)) as connection:
            with connection:
                connection.execute("""
                    CREATE TABLE login_attempts (
                        username TEXT PRIMARY KEY,
                        failed_attempts INTEGER NOT NULL DEFAULT 0,
                        locked_until REAL NOT NULL DEFAULT 0
                    )
                """)

        create_database()

        with closing(sqlite3.connect(self.database_path)) as connection:
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(login_attempts)"
                ).fetchall()
            }

        self.assertIn("updated_at", columns)


if __name__ == "__main__":
    unittest.main()
