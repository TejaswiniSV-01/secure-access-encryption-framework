
# 🔐 Secure Access & Data Encryption Framework

<p align="center">
  <strong>A hands-on cybersecurity project focused on secure authentication, multi-factor authentication, password recovery, data encryption, and vulnerability assessment.</strong>
</p>

---

## 📌 Project Overview

The **Secure Access & Data Encryption Framework** is a hands-on cybersecurity project developed to explore and implement essential security mechanisms using Python.

The project demonstrates how authentication, multi-factor authentication (MFA), password security, password recovery, file encryption, secure communication, and security testing can work together in a controlled laboratory environment.

🎯 **Main Objective:** Build a practical security framework while developing skills in Python programming, Linux, cryptography, and cybersecurity.

## 🚀 Getting Started

New to this project? Follow the [Installation and User Guide](INSTALLATION.md) to download, configure, and run the application.

The guide covers:
- Python environment setup and dependencies.
- Secret key configuration.
- Local HTTPS certificate generation.
- Running the CLI and web application.
- MFA, file encryption, and password recovery.
- Automated tests and security checks.

**Quick start:**

```bash
git clone https://github.com/TejaswiniSV-01/secure-access-encryption-framework.git
cd secure-access-encryption-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ✨ Key Features

| Feature | Description | Status |
|---|---|---|
| 🔑 Secure Authentication | User registration, login, and password hashing using Argon2 | ✅ Implemented |
| 🔐 Password Strength Validation | Enforces a minimum of 12 characters, uppercase, lowercase, numbers, and special characters | ✅ Implemented |
| 📧 Password Reset | OTP-based password recovery through email | ✅ Implemented |
| 📱 Multi-Factor Authentication | Additional verification using MFA | ✅ Implemented |
| 🔒 File Encryption | Encryption and decryption of stored files | ✅ Implemented |
| 🌐 HTTPS/TLS | Local HTTPS configuration using OpenSSL | ✅ Configured locally |
| 🛡️ Security Assessment | Static analysis and dependency vulnerability checks | ✅ Initial assessment |
| 🧪 Automated Testing | Automated unit and web application tests | ✅ Implemented |

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| Kali Linux | Development and security testing environment |
| Flask | Web application framework |
| SQLite | Database management |
| Argon2 | Secure password hashing |
| PyOTP | One-time password generation and MFA |
| Cryptography | File encryption and cryptographic operations |
| Flask-WTF | CSRF protection |
| OpenSSL | TLS certificate generation |
| Git & GitHub | Version control and project hosting |
| Bandit | Python security static analysis |
| pip-audit | Python dependency vulnerability checking |
| Nmap | Planned authorized laboratory assessment |
| Metasploit Framework | Planned authorized laboratory testing |

## 🏗️ Project Structure

```text
secure-access-encryption-framework/
│
├── app.py                         # Main application entry point
│
├── security/                      # Core security modules
│   ├── __init__.py
│   ├── authentication.py
│   ├── database.py
│   ├── email_service.py
│   ├── file_encryption.py
│   ├── mfa.py
│   ├── mfa_enrollment.py
│   ├── password_reset.py
│   ├── passwords.py
│   ├── rate_limiter.py
│   ├── registration.py
│   ├── secret_storage.py
│   └── validation.py
│
├── web/                           # Flask web application
│   ├── app.py
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── password_reset.html
│       ├── password_reset_confirm.html
│       ├── dashboard.html
│       └── index.html
│
├── tests/                         # Automated test suite
│   ├── test_app.py
│   ├── test_authentication.py
│   ├── test_database.py
│   ├── test_file_encryption.py
│   ├── test_mfa.py
│   ├── test_mfa_enrollment.py
│   ├── test_password_reset.py
│   ├── test_passwords.py
│   ├── test_rate_limiter.py
│   ├── test_registration.py
│   ├── test_secret_storage.py
│   └── test_web.py
│
├── docs/                          # Project documentation
│   └── SECURITY_ASSESSMENT.md
│
├── requirements.txt               # Application dependencies
├── requirements-dev.txt           # Development dependencies
├── .gitignore
└── README.md
```

## 🧪 Security Testing Results

The project has undergone automated testing and initial security assessment.

| Security Check | Result |
|---|---|
| Unit and web application tests | ✅ 116 tests passed |
| Password strength validation tests | ✅ Passed |
| Password reset tests | ✅ Passed |
| HTTPS login test | ✅ Successful in local environment |
| Secure session cookie configuration | ✅ Enabled |
| Bandit static analysis | ✅ Zero issues identified |
| pip-audit | ✅ No known vulnerabilities found |

> **Note:** These results represent the current development assessment. They do not guarantee that the application is free from vulnerabilities.

## 🌐 HTTPS/TLS Configuration

Local HTTPS has been configured using OpenSSL with a self-signed certificate.

- RSA 2048-bit certificate.
- Subject Alternative Names for `localhost` and `127.0.0.1`.
- Secure session cookies enabled.
- HTTP-only session cookies.
- SameSite cookie policy.
- Private key permissions restricted to the owner.

⚠️ **Important:** The self-signed certificate is intended for local development only. Production deployment still requires a trusted certificate and a production-grade WSGI server.

## 🔐 Password Security

The application includes password security and recovery mechanisms.

**Password requirements:**
- Minimum 12 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one number.
- At least one special character.

**Password recovery:**
- Users can request a password reset using their username.
- A one-time verification code (OTP) is sent to the registered email address.
- The reset code has a limited validity period.
- OTP verification includes an attempt limit.
- Users must enter and confirm their new password.

Passwords are hashed using Argon2 rather than stored as plain text.

## 🎓 Learning Objectives

Through this project, I aim to develop practical knowledge of:

- Linux commands and system administration.
- Python programming and application development.
- Secure authentication and password hashing.
- Password strength validation and recovery.
- Multi-factor authentication.
- Data encryption and cryptographic concepts.
- HTTPS/TLS and secure communications.
- Vulnerability assessment and remediation.
- Automated testing and security documentation.
- Git and GitHub workflows.

## 🚀 Project Roadmap

- [x] Initial project setup
- [x] Secure authentication
- [x] Password hashing
- [x] Strong password validation
- [x] OTP-based password reset
- [x] Password reset web interface
- [x] Password reset automated tests
- [x] Multi-factor authentication
- [x] File encryption
- [x] Flask web application
- [x] Automated security testing
- [x] Initial security assessment
- [x] Local HTTPS/TLS configuration
- [ ] Further security hardening
- [ ] Authorized laboratory vulnerability assessment
- [ ] Production deployment preparation
- [ ] Final documentation and project review

## ⚠️ Security & Ethical Use

This project is developed for educational and authorized cybersecurity testing purposes.

- Security testing is limited to systems owned by me or systems for which explicit permission has been granted.
- Private keys, passwords, tokens, and other sensitive information must never be committed to GitHub.
- Local self-signed TLS certificates must not be treated as production certificates.
- Vulnerability testing must only be performed in authorized environments.

## 👩‍💻 About This Project

This is my first hands-on cybersecurity project. I'm building it step by step to strengthen my understanding of software development and practical cybersecurity.

The goal is not just to build an application, but also to understand the security principles behind every component.

---

<p align="center">
  <strong>🔐 LEARNING • BUILDING • SECURING</strong>
  <br>
  <em>One step at a time.</em>
</p>
