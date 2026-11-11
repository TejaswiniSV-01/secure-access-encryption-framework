
import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf.csrf import CSRFProtect

from security.authentication import login_user
from security.registration import register_user
from security.password_reset import (
    request_password_reset,
    reset_password,
)
from security.mfa_enrollment import (
    begin_mfa_enrollment,
    confirm_mfa_enrollment,
)


app = Flask(__name__)

# Load the secret key from the private environment.
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "FLASK_SECRET_KEY is missing. "
        "Load it from your private environment file."
    )

# Enable CSRF protection for forms.
csrf = CSRFProtect(app)

# Session cookie security settings.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True,
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip() or None
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        success, message = register_user(
            username,
            password,
            email,
        )

        if success:
            flash(message, "success")
        else:
            flash(message, "error")

        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        mfa_code = request.form.get("mfa_code", "").strip() or None

        session.clear()

        success, message = login_user(
            username,
            password,
            mfa_code,
        )

        if success:
            session.clear()
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash(message, "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/password-reset", methods=["GET", "POST"])
def password_reset_request():
    if request.method == "POST":
        username = request.form.get("username", "").strip()

        try:
            success, message = request_password_reset(username)
            flash(message, "success" if success else "error")
        except Exception:
            flash(
                "Unable to process the request right now. Please try again later.",
                "error",
            )

        return redirect(
            url_for("password_reset_confirm", username=username)
        )

    return render_template("password_reset.html")


@app.route("/password-reset/confirm", methods=["GET", "POST"])
def password_reset_confirm():
    username = request.values.get("username", "").strip()

    if request.method == "POST":
        otp = request.form.get("otp", "").strip()
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(
                url_for("password_reset_confirm", username=username)
            )

        try:
            success, message = reset_password(
                username,
                otp,
                new_password,
            )
        except Exception:
            flash(
                "Password reset could not be completed. Please try again later.",
                "error",
            )
            return redirect(url_for("login"))

        if success:
            flash(message, "success")
            return redirect(url_for("login"))

        flash(message, "error")
        return redirect(
            url_for("password_reset_confirm", username=username)
        )

    return render_template(
        "password_reset_confirm.html",
        username=username,
    )


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
    )


@app.route("/mfa/setup", methods=["GET", "POST"])
def mfa_setup():
    if "username" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form.get("password", "")

        success, message, setup_uri = begin_mfa_enrollment(
            session["username"],
            password,
        )

        if not success:
            flash(message, "error")
            return redirect(url_for("mfa_setup"))

        return render_template(
            "mfa_setup.html",
            setup_uri=setup_uri,
        )

    return render_template("mfa_setup.html")


@app.route("/mfa/confirm", methods=["POST"])
def mfa_confirm():
    if "username" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("login"))

    password = request.form.get("password", "")
    code = request.form.get("mfa_code", "").strip()

    success, message = confirm_mfa_enrollment(
        session["username"],
        password,
        code,
    )

    if success:
        flash(message, "success")
        return redirect(url_for("dashboard"))

    flash(message, "error")
    return redirect(url_for("mfa_setup"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        ssl_context=(
            "instance/tls/localhost-cert.pem",
            "instance/tls/localhost-key.pem",
        ),
    )
