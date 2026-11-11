# Installation and User Guide

This guide explains how to download, configure, and run the Secure Access & Data Encryption Framework.

## 1. Project Requirements

The following software is required:

- Python 3
- Git
- OpenSSL
- Linux terminal (Kali Linux used for development)

## 2. Download the Project

Clone the GitHub repository:

```bash
git clone https://github.com/TejaswiniSV-01/secure-access-encryption-framework.git
```

Enter the project directory:

```bash
cd secure-access-encryption-framework
```

## 3. Create a Python Virtual Environment

Create the environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

## 4. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install application dependencies:

```bash
pip install -r requirements.txt
```

For development and security testing tools, install:

```bash
pip install -r requirements-dev.txt
```

## 5. Configure Environment Variables

The application uses two secret environment variables:
- MFA_ENCRYPTION_KEY is required when using MFA features in the CLI or web application.
- FLASK_SECRET_KEY is required to run the Flask web application.

Generate a Flask secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate a Fernet-compatible MFA encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Create a private configuration directory:

```bash
mkdir -p ~/.config/secure-access
chmod 700 ~/.config/secure-access
```

Create the environment file:

```bash
nano ~/.config/secure-access/mfa.env
```

Add the following entries, replacing the placeholders with the newly generated values:

```bash
export FLASK_SECRET_KEY="YOUR_GENERATED_FLASK_SECRET_KEY"
export MFA_ENCRYPTION_KEY="YOUR_GENERATED_FERNET_KEY"
```

Save the file and restrict its permissions:

```bash
chmod 600 ~/.config/secure-access/mfa.env
```

Load the variables into your terminal:

```bash
set -a
source ~/.config/secure-access/mfa.env
set +a
```

Never share or commit these secret values.

## 6. Configure Local HTTPS

The web application requires a local TLS certificate and private key.

Create the TLS directory:

```bash
mkdir -p instance/tls
```

Generate a self-signed RSA certificate with Subject Alternative Names:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout instance/tls/localhost-key.pem \
-out instance/tls/localhost-cert.pem \
-subj "/CN=localhost" \
-addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```

Restrict private key permissions:

```bash
chmod 600 instance/tls/localhost-key.pem
```

The generated files should be:

- `instance/tls/localhost-cert.pem`
- `instance/tls/localhost-key.pem`

These certificates are for local development only. They are not trusted production certificates.

## 7. Run the Command-Line Application

Start the CLI:

```bash
python app.py
```

The menu allows users to:

1. Register an account.
2. Log in.
3. Request a password reset.
4. Reset a password.
5. Set up and confirm MFA after login.
6. Encrypt files after login.
7. Decrypt files after login.
8. Log out or exit.

The database is initialized automatically through the registration and database operations.

## 8. Run the Web Application

First, make sure the environment variables are loaded in the terminal.

Start the Flask application:

```bash
python -m web.app
```

Open the following address in your browser:

```text
https://127.0.0.1:5000
```

Because the certificate is self-signed, your browser may display a security warning. This is expected in the local development environment.

Register an account and log in through the web interface.

## 9. Configure Password Reset Emails (Optional)

Password-reset emails use Gmail SMTP.

Create the email configuration directory:

```bash
mkdir -p ~/.config/secure-access
chmod 700 ~/.config/secure-access
```

Create the credentials file:

```bash
nano ~/.config/secure-access/email.env
```

Add:

```bash
EMAIL_ADDRESS=your-gmail-address
EMAIL_APP_PASSWORD=your-gmail-app-password
```

Save and restrict access:

```bash
chmod 600 ~/.config/secure-access/email.env
```

A Gmail app password is required. Do not use your normal Gmail password.

Email configuration is needed only for password-reset email delivery.

## 10. Run Automated Tests

Run the test suite:

```bash
python -m unittest discover -v
```

## 11. Run Security Checks

Run Bandit:

```bash
bandit -r security web app.py
```

Run dependency vulnerability checks:

```bash
pip-audit
```

## 12. Security Notes

- Use strong passwords of at least 12 characters.
- Keep Flask and MFA encryption keys private.
- Never upload private keys, database files, or email credentials to GitHub.
- Use a separate MFA encryption key for each installation.
- Back up important encrypted files and protect their encryption passwords.
- Local self-signed TLS certificates are not suitable for production.
- This project is intended for educational and authorized testing purposes.

## 13. Troubleshooting

**Missing Flask secret key**

Load the private environment file again:

```bash
set -a
source ~/.config/secure-access/mfa.env
set +a
```

**Missing MFA encryption key**

Check that `MFA_ENCRYPTION_KEY` is present in your private environment file and reload it.

**TLS certificate or key not found**

Check that both certificate files exist in `instance/tls/`.

**Email credentials are not configured**

Check that `~/.config/secure-access/email.env` exists and contains the required email configuration.

**Python dependency errors**

Activate the virtual environment and reinstall dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

**Project:** Secure Access & Data Encryption Framework  
**Purpose:** Educational cybersecurity and secure application development.
