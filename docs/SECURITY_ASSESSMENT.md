
# Secure Access & Encryption Framework
## Security Assessment Report

![Security Tests](https://img.shields.io/badge/Security_Tests-PASS-brightgreen)
![Unit Tests](https://img.shields.io/badge/Unit_Tests-88%20Passed-brightgreen)
![Bandit](https://img.shields.io/badge/Bandit-0%20Findings-brightgreen)
![Dependency Audit](https://img.shields.io/badge/pip--audit-No_Known_Vulnerabilities-brightgreen)

---

## 1. Assessment Overview

| Detail | Information |
|---|---|
| Project | Secure Access & Encryption Framework |
| Assessment Date | 5 November 2026 |
| Platform | Kali Linux |
| Programming Language | Python |
| Database | SQLite |
| Assessment Type | Application Security Assessment |
| Testing Approach | Automated and Manual Testing |

### Objective

The objective of this assessment is to evaluate the security features implemented in the Secure Access & Encryption Framework.

The assessment focuses on authentication, password protection, multi-factor authentication, password recovery, file encryption, database security, and dependency vulnerabilities.

---

## 2. Security Features Implemented

| Security Feature | Implementation | Status |
|---|---|---|
| Username Validation | Input validation rules | PASS |
| Password Hashing | Argon2 | PASS |
| User Authentication | Password verification | PASS |
| Multi-Factor Authentication | TOTP | PASS |
| MFA Secret Protection | Fernet encryption | PASS |
| Login Rate Limiting | 5 failed attempts, 5-minute lockout | PASS |
| Password Reset | OTP-based password recovery | PASS |
| OTP Protection | Argon2 hashing, expiry and attempt limits | PASS |
| Email Delivery | Gmail SMTP over SSL | PASS |
| File Encryption | AES-256-GCM | PASS |
| Key Derivation | Scrypt | PASS |
| Database Protection | SQLite permissions and migrations | PASS |

---

## 3. Security Testing Results

### 3.1 Automated Unit Testing

The Python unit test suite was executed using:

```bash
python -m unittest discover -v
```

**Result: 88 tests passed.**

| Test Result | Count |
|---|---:|
| Tests Executed | 88 |
| Tests Passed | 88 |
| Tests Failed | 0 |

The tests cover application functionality and security-related behaviour, including authentication, MFA, password handling, password recovery, database operations, and file encryption.

### 3.2 Static Application Security Testing

The Bandit security scanner was executed using:

```bash
bandit -r . -x ./.venv,./tests
```

**Result: No issues identified.**

| Scan Detail | Result |
|---|---:|
| Lines of Code Scanned | 1,072 |
| High Severity Findings | 0 |
| Medium Severity Findings | 0 |
| Low Severity Findings | 0 |
| Undefined Severity Findings | 0 |

**Scope note:** The virtual environment and test directory were excluded from this scan. The result applies to the scanned application code, not every file in the repository.

### 3.3 Dependency Vulnerability Assessment

The dependency audit was performed using:

```bash
pip-audit
```

**Result: No known vulnerabilities found.**

The audit did not identify known vulnerabilities in the installed Python dependencies.

---

## 4. Manual Security Verification

The following security behaviours were manually checked during development.

| Security Check | Expected Behaviour | Result |
|---|---|---|
| User Registration | Valid registration succeeds | PASS |
| User Login | Correct credentials allow login | PASS |
| MFA Enrollment | Password verification is required | PASS |
| MFA Confirmation | Valid TOTP code enables MFA | PASS |
| MFA Login | Valid authenticator code is accepted | PASS |
| Invalid MFA Code | Invalid code does not enable MFA | PASS |
| Login Rate Limiting | Repeated failed attempts trigger lockout | PASS |
| Password Reset OTP | OTP is verified before password reset | PASS |
| OTP Expiration | Expired OTP is rejected | PASS |
| OTP Reuse | Previously used OTP is rejected | PASS |
| OTP Storage | OTP is stored as a hash | PASS |
| File Encryption | Sample file is encrypted successfully | PASS |
| File Decryption | Correct password decrypts the file | PASS |
| File Integrity | Decrypted file matches original content | PASS |
| Incorrect File Password | Incorrect password cannot decrypt the file | PASS |
| Failed Decryption | No output file is created after failed decryption | PASS |
| Database Permissions | Database file has restricted permissions | PASS |

---

## 5. Security Controls and Design

### Password Security

- Passwords are hashed using Argon2.
- Password verification is performed during authentication.
- Plain-text passwords are not stored in the user database.

### Multi-Factor Authentication

- TOTP is used as the second authentication factor.
- MFA secrets are encrypted using Fernet before database storage.
- Password verification is required to begin and confirm MFA enrollment.

### Authentication Protection

- Login attempts are rate-limited.
- Five failed attempts trigger a five-minute lockout.
- Authentication responses are designed to avoid unnecessarily revealing account information.

### Password Recovery

- Password-reset OTPs are generated using a cryptographically secure random generator.
- OTPs are stored as Argon2 hashes.
- OTPs expire after five minutes.
- A maximum of five verification attempts is allowed.
- Successfully used OTPs cannot be reused.

### File Encryption

- AES-256-GCM provides authenticated file encryption.
- Scrypt is used for password-based key derivation.
- Authentication protects encrypted file contents against undetected modification.
- Incorrect passwords are rejected during decryption.
- Existing output files are not overwritten.

### Database Security

- SQLite is used for data storage.
- Database migrations support schema updates.
- Database connections are cleaned up.
- Database file permissions are restricted.

---

## 6. Security Configuration

Sensitive configuration values are stored outside the project repository.

Examples include:

- MFA encryption key.
- Email account credentials.
- Email application password.

File permissions are restricted to reduce unauthorized access.

**Important:** Secret keys and credentials must never be committed to GitHub or included in source code.

---

## 7. Limitations and Areas for Improvement

| Area | Recommendation | Priority |
|---|---|---|
| Session Management | Implement secure session handling | High |
| HTTPS/TLS | Add HTTPS when developing the web application | High |
| File Encryption | Support large files without loading the entire file into memory | Medium |
| Key Management | Introduce secure key rotation and backup procedures | High |
| Logging | Add security event logging without exposing secrets | Medium |
| Deployment | Perform additional security testing in a production-like environment | High |
| Recovery | Define a secure MFA recovery process | Medium |

The current command-line application uses an in-process login state. This should not be treated as production-grade session management.

---

## 8. Overall Assessment

**TESTS PASSED**

The Secure Access & Encryption Framework implements several important security controls, including:

- Argon2 password hashing.
- TOTP multi-factor authentication.
- Fernet encryption for stored MFA secrets.
- Login rate limiting.
- Secure OTP-based password recovery.
- AES-256-GCM file encryption.
- Scrypt-based key derivation.
- Restricted database and configuration file permissions.

### Latest Validation Results

| Assessment | Result |
|---|---|
| Python Unit Tests | 88 Passed |
| Bandit Application Code Scan | 0 Findings |
| Bandit Lines Scanned | 1,072 |
| pip-audit | No Known Vulnerabilities |
| Manual Security Checks | Passed |

Passing automated and manual tests does not guarantee that an application is completely secure. Further testing, code review, and security improvements are necessary before production deployment.

---

## 9. Conclusion

This project demonstrates the implementation of fundamental application security concepts using Python.

It provides practical experience with authentication, password hashing, multi-factor authentication, encryption, database security, vulnerability scanning, and software testing.

The project will continue to evolve with additional security improvements, web application development, HTTPS/TLS configuration, and further testing.

---

*Report prepared for the Secure Access & Encryption Framework project.*

*Assessment Date: 5 November 2026*
