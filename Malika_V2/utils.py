import os
import uuid

from config import Config
from werkzeug.utils import secure_filename


def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in Config.ALLOWED_EXTENSIONS
    )


def save_image(file):

    if not file:
        return None

    if file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    extension = file.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4().hex}.{extension}"

    filename = secure_filename(filename)

    path = os.path.join(
        Config.UPLOAD_FOLDER,
        filename
    )

    os.makedirs(
        Config.UPLOAD_FOLDER,
        exist_ok=True
    )

    file.save(path)

    return filename


def format_currency(amount):

    return f"KES {amount:,.2f}"


def cart_total(cart):

    return sum(
        item["price"] * item["quantity"]
        for item in cart
    )
    from datetime import datetime, timedelta
from database import get_db


def check_login_attempts(ip):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT attempts, lockout_until
        FROM login_attempts
        WHERE ip=%s
        """,
        (ip,)
    )

    record = cur.fetchone()

    cur.close()
    conn.close()

    if not record:
        return True

    if record["lockout_until"]:

        if record["lockout_until"] > datetime.now():
            return False

    return True


def record_failed_login(ip):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT attempts
        FROM login_attempts
        WHERE ip=%s
        """,
        (ip,)
    )

    record = cur.fetchone()

    if record:

        attempts = record["attempts"] + 1

        lockout = None

        if attempts >= 5:
            lockout = datetime.now() + timedelta(minutes=15)

        cur.execute(
            """
            UPDATE login_attempts
            SET attempts=%s,
                lockout_until=%s
            WHERE ip=%s
            """,
            (
                attempts,
                lockout,
                ip
            )
        )

    else:

        cur.execute(
            """
            INSERT INTO login_attempts(
                ip,
                attempts
            )
            VALUES(%s,%s)
            """,
            (
                ip,
                1
            )
        )

    conn.commit()

    cur.close()
    conn.close()


def clear_login_attempts(ip):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM login_attempts
        WHERE ip=%s
        """,
        (ip,)
    )

    conn.commit()

    cur.close()
    conn.close()
