
import sqlite3
import time
from contextlib import closing

from security import database


DATABASE_PATH = database.DATABASE_PATH

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_SECONDS = 300
DEFAULT_ATTEMPT_RETENTION_SECONDS = 30 * 24 * 60 * 60


class RateLimiterError(RuntimeError):
    """Raised when a rate-limiter database operation fails."""


def _validate_username(username):
    """Validate usernames before database operations."""
    if not isinstance(username, str) or not username.strip():
        raise ValueError("A valid username is required.")


def _prepare_database():
    """Ensure the database is ready for rate-limiter operations."""
    try:
        database.create_database()
    except sqlite3.Error as error:
        raise RateLimiterError(
            "Could not prepare the rate-limiter database."
        ) from error


def is_locked(username, now=None):
    """Check whether a username is currently locked."""
    _validate_username(username)

    if now is None:
        now = time.time()

    _prepare_database()

    try:
        with closing(
            sqlite3.connect(database.DATABASE_PATH)
        ) as connection:
            result = connection.execute(
                """
                SELECT locked_until
                FROM login_attempts
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        return result is not None and result[0] > now

    except sqlite3.Error as error:
        raise RateLimiterError(
            "Could not check account lockout status."
        ) from error


def record_failed_attempt(username, now=None):
    """Record a failed login and enforce the lockout policy."""
    _validate_username(username)

    if now is None:
        now = time.time()

    _prepare_database()

    try:
        with closing(
            sqlite3.connect(database.DATABASE_PATH)
        ) as connection:

            connection.execute("BEGIN IMMEDIATE")

            try:
                result = connection.execute(
                    """
                    SELECT failed_attempts, locked_until
                    FROM login_attempts
                    WHERE username = ?
                    """,
                    (username,),
                ).fetchone()

                if result is None:
                    failed_attempts = 0
                    locked_until = 0

                else:
                    failed_attempts, locked_until = result

                    # Ignore attempts while the account is locked.
                    if locked_until > now:
                        connection.commit()
                        return True

                    # Reset the counter after an expired lockout.
                    if locked_until > 0 and locked_until <= now:
                        failed_attempts = 0

                failed_attempts += 1

                if failed_attempts >= MAX_FAILED_ATTEMPTS:
                    locked_until = now + LOCKOUT_SECONDS
                else:
                    locked_until = 0

                connection.execute(
                    """
                    INSERT INTO login_attempts (
                        username,
                        failed_attempts,
                        locked_until,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(username)
                    DO UPDATE SET
                        failed_attempts = excluded.failed_attempts,
                        locked_until = excluded.locked_until,
                        updated_at = excluded.updated_at
                    """,
                    (
                        username,
                        failed_attempts,
                        locked_until,
                        now,
                    ),
                )

                connection.commit()

                return locked_until > now

            except Exception:
                connection.rollback()
                raise

    except sqlite3.Error as error:
        raise RateLimiterError(
            "Could not record the failed login attempt."
        ) from error


def reset_failed_attempts(username):
    """Clear failed login attempts after successful authentication."""
    _validate_username(username)

    _prepare_database()

    try:
        with closing(
            sqlite3.connect(database.DATABASE_PATH)
        ) as connection:
            with connection:
                connection.execute(
                    """
                    DELETE FROM login_attempts
                    WHERE username = ?
                    """,
                    (username,),
                )

        return True

    except sqlite3.Error as error:
        raise RateLimiterError(
            "Could not reset failed login attempts."
        ) from error


def cleanup_old_attempts(
    max_age_seconds=DEFAULT_ATTEMPT_RETENTION_SECONDS,
    now=None,
):
    """Remove old inactive login-attempt records."""

    if (
        isinstance(max_age_seconds, bool)
        or not isinstance(max_age_seconds, (int, float))
    ):
        raise ValueError("Retention period must be a number.")

    if max_age_seconds <= 0:
        raise ValueError("Retention period must be positive.")

    if now is None:
        now = time.time()

    cutoff = now - max_age_seconds

    _prepare_database()

    try:
        with closing(
            sqlite3.connect(database.DATABASE_PATH)
        ) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    DELETE FROM login_attempts
                    WHERE updated_at < ?
                    AND locked_until <= ?
                    """,
                    (cutoff, now),
                )

                deleted_count = cursor.rowcount

        return deleted_count

    except sqlite3.Error as error:
        raise RateLimiterError(
            "Could not clean up old login-attempt records."
        ) from error

