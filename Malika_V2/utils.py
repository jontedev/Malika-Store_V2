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