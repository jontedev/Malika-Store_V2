from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import (
    create_user,
    get_user_by_email
)

from utils import (
    check_login_attempts,
    failed_attempt,
    reset_attempts,
    login_attempts_count
)

from config import Config


auth = Blueprint("auth", __name__)


# ==========================================
# USER REGISTER
# ==========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if session.get("user"):
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        existing_user = get_user_by_email(email)

        if existing_user:

            return render_template(
                "register.html",
                error="Email already exists."
            )

        hashed_password = generate_password_hash(password)

        create_user(
            name,
            email,
            hashed_password
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# USER LOGIN
# ==========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user"):
        return redirect(
            url_for("home")
        )

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        user = get_user_by_email(email)

        if not user:

            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        if not check_password_hash(
            user["password"],
            password
        ):

            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        session["user"] = {

            "id": user["id"],
            "name": user["name"],
            "email": user["email"]

        }

        return redirect(
            url_for("home")
        )
# ==========================================
# USER LOGOUT
# ==========================================

@auth.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(
        url_for("home")
    )


# ==========================================
# ADMIN LOGIN
# ==========================================

@auth.route("/mk-dashboard/login", methods=["GET", "POST"])
def admin_login():

    ip = request.remote_addr

    allowed, remaining = check_login_attempts(ip)

    if not allowed:

        return render_template(
            "admin_login.html",
            error=f"Too many attempts. Try again in {remaining} minutes."
        )

    if request.method == "POST":

        password = request.form["password"]

        if password == Config.ADMIN_PASSWORD:

            reset_attempts(ip)

            session["admin"] = True

            return redirect(
                url_for("admin.dashboard")
            )

        failed_attempt(ip)

        allowed, remaining = check_login_attempts(ip)

        if not allowed:

            return render_template(
                "admin_login.html",
                error="Too many attempts. Locked for 6 hours."
            )

        attempts_left = max(0, 5 - login_attempts_count(ip))

        return render_template(
            "admin_login.html",
            error=f"Wrong password. {attempts_left} attempts remaining."
        )

    return render_template(
        "admin_login.html"
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@auth.route("/mk-dashboard/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(
        url_for("auth.admin_login")
    )
    