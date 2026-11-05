# Security Assessment
## Secure Access & Encryption Framework

**Assessment date:** 5 November 2026
**Project status:** Development and security testing
**Application:** Python CLI and Flask web interface

---

## 1. Project Overview

The Secure Access & Encryption Framework is a learning project designed to demonstrate secure authentication, multi-factor authentication (MFA), password protection, and file encryption.

The project includes:

- User registration and authentication.
- Secure password hashing using Argon2.
- Time-based one-time password (TOTP) multi-factor authentication.
- Encrypted storage of MFA secrets.
- Login rate limiting.
- Password reset using email OTP verification.
- AES-256-GCM file encryption and decryption.
- A Flask-based web interface.
- Automated unit and web application tests.

## 2. Security Features Implemented

### 2.1 Password Security

- Passwords are hashed using Argon2.
- Plaintext passwords are not stored in the database.
- Password verification uses the Argon2 verification process.
- Registration requires a minimum password length of 12 characters.
- Password reset updates the stored password hash.

### 2.2 Authentication

- User authentication verifies the username and password.
- Generic authentication error messages help reduce username enumeration.
- Login attempts are rate-limited.
- Five failed login attempts trigger a five-minute lockout.
- Successful authentication resets failed-attempt tracking.

### 2.3 Multi-Factor Authentication

- TOTP-based MFA is implemented using PyOTP.
- MFA secrets are encrypted using Fernet before database storage.
- MFA enrollment requires the user's account password.
- MFA is enabled only after successful verification of an authenticator code.
- Login requires a valid MFA code when MFA is enabled.
- Invalid and missing MFA codes are rejected.

### 2.4 Password Reset

- Password reset uses a six-digit OTP.
- OTP values are generated using a cryptographically secure random generator.
- OTP values are stored as Argon2 hashes.
- OTPs expire after five minutes.
- A maximum of five incorrect attempts is permitted.
- Successfully used OTPs cannot be reused.
- Generic responses help prevent account enumeration.

### 2.5 File Encryption

- Files are encrypted using AES-256-GCM.
- Scrypt is used for password-based key derivation.
- Authentication protects encrypted file contents against undetected modification.
- Incorrect passwords are rejected.
- Tampered encrypted files are rejected.
- Existing output files are not overwritten.
- Failed decryption does not create an output file.

### 2.6 Web Application Security

The project includes a Flask web interface with:

- User registration and login.
- Authenticated dashboard access.
- Web-based MFA enrollment and confirmation.
- Logout functionality.
- CSRF protection using Flask-WTF.
- Signed Flask sessions.
- HTTP-only session cookies.
- `SameSite=Lax` session cookie configuration.
- Debug mode disabled.
- Local development server restricted to `127.0.0.1`.

The session stores the authenticated username, not the user's password or MFA secret.

## 3. Security Configuration

### 3.1 Database Protection

- The SQLite database file is configured with restrictive file permissions.
- Database operations use parameterized SQL queries.
- Database connections are closed using context managers and cleanup mechanisms.
- Database schema migrations preserve existing data.

### 3.2 Secret Management

- MFA encryption keys are stored outside the project directory.
- Flask session signing keys are stored outside the project directory.
- Email credentials are stored in a private configuration directory.
- Sensitive configuration files use restrictive permissions.
- Private keys and credentials are excluded from version control.

### 3.3 Session and Cookie Configuration

The Flask application currently uses:

| Setting | Configuration |
|---|---|
| HTTPOnly | Enabled |
| SameSite | Lax |
| Secure | Disabled for local HTTP testing |
| Debug mode | Disabled |
| Server binding | 127.0.0.1 |

**Important limitation:** The application currently runs over local HTTP. HTTPS/TLS has not yet been configured. The Secure cookie setting must be enabled when HTTPS is deployed.

## 4. Automated Testing Results

The complete automated test suite was executed using:

`python -m unittest discover -v`

**Result: 105 tests passed.**

| Test category | Tests |
|---|---:|
| CLI application and validation | 13 |
| Authentication | 12 |
| Database | 4 |
| File encryption | 6 |
| MFA | 6 |
| MFA enrollment | 6 |
| Password reset | 14 |
| Password security | 6 |
| Rate limiter | 13 |
| Secret storage | 4 |
| Flask web application | 17 |
| **Total** | **105** |

All tests passed with zero failures and zero errors.

### 4.1 Flask Web Application Tests

The 17 web tests cover:

- Homepage loading.
- Registration page loading.
- Successful registration.
- Password mismatch handling.
- Login page loading.
- Successful login.
- Failed login.
- Dashboard access protection.
- Authenticated dashboard access.
- Logout and session clearing.
- CSRF protection.
- MFA setup access protection.
- MFA confirmation access protection.
- Successful MFA setup.
- Successful MFA confirmation.
- Failed MFA confirmation.

MFA route tests use mocked enrollment and confirmation functions. They verify route behaviour without changing real account MFA settings.

### 4.2 Manual Web Testing

The following web application behaviours were manually verified:

| Test | Result |
|---|---|
| Homepage opens | PASS |
| Registration works | PASS |
| Password mismatch is rejected | PASS |
| Login works | PASS |
| Dashboard displays authenticated username | PASS |
| Logout clears access | PASS |
| Dashboard requires authentication | PASS |
| MFA enrollment succeeds | PASS |
| Login without MFA code is rejected for an MFA-enabled account | PASS |
| Login with valid MFA code succeeds | PASS |

## 5. Static Security Analysis

### 5.1 Bandit

Command executed:

`bandit -r . -x ./.venv,./tests`

Latest result:

| Metric | Result |
|---|---:|
| Lines of code scanned | 1,202 |
| High severity findings | 0 |
| Medium severity findings | 0 |
| Low severity findings | 0 |
| Total findings | 0 |

**Result:** No issues identified.

The virtual environment and test directory were excluded from this scan.

### 5.2 Dependency Vulnerability Audit

Command executed:

`pip-audit`

Latest result:

**No known vulnerabilities found.**

This result reflects the installed dependencies checked at the time of the audit.

## 6. Security Limitations and Future Improvements

The project is still under development. The following improvements remain:

| Area | Planned improvement | Priority |
|---|---|---|
| HTTPS/TLS | Configure HTTPS for web communications | High |
| Session security | Enable Secure cookies after HTTPS deployment | High |
| Web deployment | Use a production WSGI server | High |
| Web password reset | Add password reset to the web interface | Medium |
| Web file encryption | Add file encryption and decryption to the web interface | Medium |
| Session lifecycle | Improve session expiration and lifecycle management | Medium |
| Logging | Improve security event logging and monitoring | Medium |
| MFA usability | Improve the MFA setup and confirmation interface | Medium |
| Security testing | Expand automated web security tests | Medium |

### 6.1 Current Deployment Limitations

- The Flask development server is intended for local development, not production deployment.
- HTTPS/TLS is not yet configured.
- The session cookie Secure flag is disabled for local HTTP testing.
- Web-based password reset and file encryption are not yet implemented.
- Additional production security testing is required.

## 7. Overall Assessment

The project currently implements several important security controls, including password hashing, multi-factor authentication, encrypted secret storage, login rate limiting, secure password reset, and authenticated file encryption.

The Flask interface provides browser-based registration, authentication, dashboard access, logout, and MFA enrollment.

The latest verification results are:

| Security check | Result |
|---|---|
| Automated tests | 105 passed |
| Flask web tests | 17 passed |
| Bandit | 0 issues identified |
| Bandit lines scanned | 1,202 |
| pip-audit | No known vulnerabilities |
| Manual MFA verification | Passed |

These results demonstrate that the tested functionality is working as expected. They do not constitute a complete security audit or establish production readiness.

## 8. Conclusion

The Secure Access & Encryption Framework has progressed from a command-line security application to an application with both CLI and Flask web interfaces.

Core authentication, encryption, MFA, and password-reset functionality has been implemented and tested.

Future development will focus on HTTPS/TLS, production deployment, additional web features, improved session management, and further security testing.
