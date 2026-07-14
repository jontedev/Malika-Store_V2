from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models import (
    get_products,
    get_product,
    get_categories,
    create_product,
    update_product,
    delete_product,
    get_orders,
    update_order_status,
    total_products,
    total_orders,
    total_users,
    total_revenue
)

from utils import (
    save_image,
    format_currency
)


admin = Blueprint("admin", __name__)


# ==========================================
# ADMIN AUTH
# ==========================================

def admin_required():

    if not session.get("admin"):

        return False

    return True


@admin.before_request
def protect_admin():

    if not admin_required():

        return redirect(
            url_for("auth.admin_login")
        )


# ==========================================
# DASHBOARD
# ==========================================

@admin.route("/mk-dashboard")
def dashboard():

    return render_template(

        "admin/dashboard.html",

        total_products=total_products(),

        total_orders=total_orders(),

        total_users=total_users(),

        revenue=total_revenue(),

        format_currency=format_currency

    )


# ==========================================
# PRODUCTS
# ==========================================

@admin.route("/mk-dashboard/products")
def products():

    return render_template(

        "admin/products.html",

        products=get_products(),

        format_currency=format_currency

    )
# ==========================================
# ADD PRODUCT
# ==========================================

@admin.route("/mk-dashboard/products/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        image = save_image(
            request.files.get("image")
        )

        create_product(

            request.form["name"].strip(),

            request.form.get("description", "").strip(),

            float(request.form["price"]),

            image,

            int(request.form["category"]),

            int(request.form["stock"]),

            "featured" in request.form

        )

        return redirect(
            url_for("admin.products")
        )

    return render_template(

        "admin/add_product.html",

        categories=get_categories()

    )


# ==========================================
# EDIT PRODUCT
# ==========================================

@admin.route("/mk-dashboard/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    product = get_product(product_id)

    if not product:

        return redirect(
            url_for("admin.products")
        )

    if request.method == "POST":

        image = save_image(
            request.files.get("image")
        )

        update_product(

            product_id,

            request.form["name"].strip(),

            request.form.get("description", "").strip(),

            float(request.form["price"]),

            image,

            int(request.form["category"]),

            int(request.form["stock"]),

            "featured" in request.form

        )

        return redirect(
            url_for("admin.products")
        )

    return render_template(

        "admin/edit_product.html",

        product=product,

        categories=get_categories()

    )


# ==========================================
# DELETE PRODUCT
# ==========================================

@admin.route("/mk-dashboard/products/delete/<int:product_id>", methods=["POST"])
def remove_product(product_id):

    delete_product(product_id)

    return redirect(
        url_for("admin.products")
    )


# ==========================================
# ORDERS
# ==========================================

@admin.route("/mk-dashboard/orders")
def orders():

    return render_template(

        "admin/orders.html",

        orders=get_orders(),

        format_currency=format_currency

    )


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@admin.route("/mk-dashboard/orders/<int:order_id>/status", methods=["POST"])
def order_status(order_id):

    status = request.form["status"]

    update_order_status(

        order_id,

        status

    )

    return redirect(
        url_for("admin.orders")
    )