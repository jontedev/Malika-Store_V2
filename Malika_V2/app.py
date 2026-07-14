import os
import uuid
import time
import logging

from pathlib import Path
from datetime import timedelta
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    session,
    jsonify,
    abort,
    g
)

from flask_login import (
    LoginManager,
    current_user
)

from flask_wtf.csrf import CSRFProtect
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from database import init_db, get_connection
from seed import seed_database

from auth import auth
from cart import cart
from admin import admin

from models import (
    get_products,
    get_product,
    get_categories,
    get_products_by_category,
    search_products,
    count_products,
    count_orders,
    count_customers,
    get_user
)

from utils import format_currency

load_dotenv()

APP_NAME = "Malika Store"
APP_VERSION = "2.0.0"

UPLOAD_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp"
}

LOG_PATH = Path("logs")
MAINTENANCE_FILE = Path("maintenance.flag")

csrf = CSRFProtect()
compress = Compress()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        "300/hour",
        "60/minute"
    ]
)

login_manager = LoginManager()


def allowed_image(filename):
    return (
        Path(filename)
        .suffix
        .lower()
        in UPLOAD_EXTENSIONS
    )


def request_time():
    return round(
        time.time() - g.start_time,
        4
    )


def maintenance_mode():
    return MAINTENANCE_FILE.exists()


def database_ok():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


def configure_logging(app):

    LOG_PATH.mkdir(
        exist_ok=True
    )

    logfile = LOG_PATH / "malika.log"

    handler = RotatingFileHandler(
        logfile,
        maxBytes=2 * 1024 * 1024,
        backupCount=10
    )

    handler.setFormatter(

        logging.Formatter(

            "[%(asctime)s] "

            "%(levelname)s "

            "%(message)s"

        )

    )

    if not app.logger.handlers:
        app.logger.addHandler(
            handler
        )

    app.logger.setLevel(
        logging.INFO
    )


def validate_config(app):

    required = [

        "SECRET_KEY",

        "UPLOAD_FOLDER"

    ]

    for item in required:

        if not app.config.get(item):

            raise RuntimeError(

                f"Missing {item}"

            )

    Path(

        app.config["UPLOAD_FOLDER"]

    ).mkdir(

        parents=True,

        exist_ok=True

    )


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        app.config["SECRET_KEY"]
    )

    app.config["UPLOAD_FOLDER"] = os.getenv(
        "UPLOAD_FOLDER",
        app.config["UPLOAD_FOLDER"]
    )

    app.config["MAX_CONTENT_LENGTH"] = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            5 * 1024 * 1024
        )
    )

    app.config.update(

        SESSION_COOKIE_HTTPONLY=True,

        SESSION_COOKIE_SAMESITE="Lax",

        SESSION_COOKIE_SECURE=not app.debug,

        REMEMBER_COOKIE_HTTPONLY=True,

        PERMANENT_SESSION_LIFETIME=timedelta(days=7)

    )

    app.wsgi_app = ProxyFix(

        app.wsgi_app,

        x_for=1,

        x_proto=1,

        x_host=1,

        x_port=1,

        x_prefix=1

    )

    validate_config(app)

    configure_logging(app)

    csrf.init_app(app)

    compress.init_app(app)

    limiter.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message_category = "warning"

    init_db()

    if app.debug:
        seed_database()

    app.register_blueprint(auth)

    app.register_blueprint(cart)

    app.register_blueprint(admin)

    @login_manager.user_loader
    def load_user(user_id):

        try:

            return get_user(
                int(user_id)
            )

        except Exception:

            return None
        @app.before_request
def before_request():

        session.permanent = True

        g.request_id = str(uuid.uuid4())

        g.start_time = time.time()

        g.current_user = current_user

        if (
            maintenance_mode()
            and not request.path.startswith("/static")
            and not request.path.startswith("/mk-dashboard")
        ):
            return render_template(
                "maintenance.html"
            ), 503

        if (
            request.content_length
            and request.content_length >
            app.config["MAX_CONTENT_LENGTH"]
        ):
            abort(413)

    @app.after_request
    def after_request(response):

        duration = request_time()

        response.headers["Server"] = (
            f"{APP_NAME}/{APP_VERSION}"
        )

        response.headers["X-Request-ID"] = (
            g.request_id
        )

        response.headers["X-Response-Time"] = (
            f"{duration:.4f}s"
        )

        response.headers["X-Frame-Options"] = (
            "SAMEORIGIN"
        )

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        response.headers[
            "Permissions-Policy"
        ] = (
            "camera=(),"
            "microphone=(),"
            "geolocation=()"
        )

        response.headers[
            "Cross-Origin-Resource-Policy"
        ] = "same-origin"

        response.headers[
            "Cross-Origin-Opener-Policy"
        ] = "same-origin"

        response.headers[
            "Content-Security-Policy"
        ] = (
            "default-src 'self';"
            "img-src 'self' data: https:;"
            "script-src 'self' 'unsafe-inline';"
            "style-src 'self' 'unsafe-inline';"
            "font-src 'self' data:;"
            "object-src 'none';"
            "base-uri 'self';"
            "frame-ancestors 'self';"
        )

        if request.path.startswith("/static"):

            response.cache_control.public = True

            response.cache_control.max_age = 86400

        else:

            response.cache_control.no_store = True

        app.logger.info(

            "%s %s %s %.3fs",

            request.method,

            request.path,

            response.status_code,

            duration

        )

        if duration > 2:

            app.logger.warning(

                "Slow request %.2fs %s",

                duration,

                request.path

            )

        return response

    @app.context_processor
    def inject_globals():

        cart = session.get("cart", {})

        return {

            "APP_NAME": APP_NAME,

            "APP_VERSION": APP_VERSION,

            "categories": get_categories(),

            "cart_count": sum(cart.values()),

            "current_user": current_user,

            "format_currency": format_currency,

            "dashboard": {

                "products": count_products(),

                "orders": count_orders(),

                "customers": count_customers()

            }

        }

    @app.template_filter("currency")
    def currency(value):

        return format_currency(value)

    @app.template_filter("upper")
    def upper(value):

        return str(value).upper()

    @app.template_filter("lower")
    def lower(value):

        return str(value).lower()

    @app.template_filter("titlecase")
    def titlecase(value):

        return str(value).title()

    @app.template_filter("yesno")
    def yesno(value):

        return "Yes" if value else "No"

    @app.template_filter("stock")
    def stock(stock):

        try:

            stock = int(stock)

        except Exception:

            return "Unknown"

        if stock <= 0:

            return "Out of Stock"

        if stock <= 5:

            return "Low Stock"

        return "In Stock"

    @app.template_filter("datetime")
    def datetime_filter(value, fmt="%d %b %Y %H:%M"):

        try:

            return value.strftime(fmt)

        except Exception:

            return value

    app.jinja_env.globals.update(

        active_page=lambda endpoint:
        request.endpoint == endpoint,

        current_year=lambda:
        time.localtime().tm_year,

        maintenance_mode=maintenance_mode,

        database_ok=database_ok,

        allowed_image=allowed_image

    )

    @limiter.request_filter
    def exempt_localhost():

        return request.remote_addr in (

            "127.0.0.1",

            "::1"

        )

    @limiter.limit("20/minute")
    @app.route("/search")
    def search():

        query = request.args.get(

            "q",

            ""

        ).strip()

        if not query:

            return redirect(

                url_for("products")

            )

        return render_template(

            "products.html",

            products=search_products(query),

            search=query,

            page_title="Search Results"

        )
        @app.route("/")
    def home():

        return render_template(

            "index.html",

            products=get_products(featured=True)

        )

    @app.route("/products")
    def products():

        return render_template(

            "products.html",

            products=get_products(),

            page_title="Products"

        )

    @app.route("/product/<int:product_id>")
    def product(product_id):

        item = get_product(product_id)

        if not item:

            abort(404)

        return render_template(

            "product.html",

            product=item

        )

    @app.route("/category/<int:category_id>")
    def category(category_id):

        return render_template(

            "products.html",

            products=get_products_by_category(category_id),

            page_title="Category"

        )

    @app.route("/about")
    def about():

        return render_template(

            "about.html"

        )

    @app.route("/contact")
    def contact():

        return render_template(

            "contact.html"

        )

    @app.route("/health")
    def health():

        return jsonify({

            "status": "healthy",

            "database": database_ok(),

            "version": APP_VERSION

        })

    @app.route("/ready")
    def ready():

        return jsonify({

            "ready": database_ok()

        })

    @app.route("/version")
    def version():

        return jsonify({

            "application": APP_NAME,

            "version": APP_VERSION

        })

    @app.route("/favicon.ico")
    def favicon():

        return send_from_directory(

            "static",

            "favicon.ico"

        )

    @app.route("/robots.txt")
    def robots():

        return send_from_directory(

            "static",

            "robots.txt"

        )

    @app.route("/sitemap.xml")
    def sitemap():

        return render_template(

            "sitemap.xml",

            products=get_products(),

            categories=get_categories()

        ), 200, {

            "Content-Type":

            "application/xml"

        }

    @app.route("/api/upload/check", methods=["POST"])
    @limiter.limit("10/minute")
    def upload_check():

        image = request.files.get("image")

        if not image:

            return jsonify({

                "success": False,

                "message": "No image uploaded."

            }), 400

        if not allowed_image(image.filename):

            return jsonify({

                "success": False,

                "message": "Invalid image."

            }), 400

        return jsonify({

            "success": True

        })

    @app.cli.command("init-db")
    def init_database():

        init_db()

        print("Database initialized.")

    @app.cli.command("seed")
    def seed():

        seed_database()

        print("Database seeded.")

    @app.cli.command("maintenance-on")
    def maintenance_on():

        MAINTENANCE_FILE.touch()

        print("Maintenance mode enabled.")

    @app.cli.command("maintenance-off")
    def maintenance_off():

        if MAINTENANCE_FILE.exists():

            MAINTENANCE_FILE.unlink()

        print("Maintenance mode disabled.")

    @app.errorhandler(400)
    def bad_request(error):

        return render_template(

            "400.html",

            error=error

        ), 400

    @app.errorhandler(401)
    def unauthorized(error):

        return render_template(

            "401.html",

            error=error

        ), 401

    @app.errorhandler(403)
    def forbidden(error):

        return render_template(

            "403.html",

            error=error

        ), 403

    @app.errorhandler(404)
    def not_found(error):

        return render_template(

            "404.html",

            error=error

        ), 404

    @app.errorhandler(405)
    def method_not_allowed(error):

        return render_template(

            "405.html",

            error=error

        ), 405

    @app.errorhandler(413)
    def request_entity_too_large(error):

        return render_template(

            "413.html",

            error=error

        ), 413

    @app.errorhandler(429)
    def rate_limit(error):

        return render_template(

            "429.html",

            error=error

        ), 429

    @app.errorhandler(500)
    def internal_server_error(error):

        app.logger.exception(error)

        return render_template(

            "500.html",

            error=error

        ), 500

    @app.errorhandler(503)
    def service_unavailable(error):

        return render_template(

            "503.html",

            error=error

        ), 503
    app.logger.info(

        "%s v%s started successfully.",

        APP_NAME,

        APP_VERSION

    )

    return app


app = create_app()

application = app


if __name__ == "__main__":

    host = os.getenv(

        "HOST",

        "0.0.0.0"

    )

    port = int(

        os.getenv(

            "PORT",

            5000

        )

    )

    debug = os.getenv(

        "FLASK_DEBUG",

        "false"

    ).lower() in (

        "1",

        "true",

        "yes"

    )

    app.run(

        host=host,

        port=port,

        debug=debug,

        threaded=True,

        use_reloader=debug

    )
