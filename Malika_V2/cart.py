from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models import (
    get_product,
    create_order,
    add_order_item
)

from utils import (
    cart_total,
    format_currency
)


cart = Blueprint("cart", __name__)


# ==========================================
# GET CART
# ==========================================

def get_cart():

    if "cart" not in session:

        session["cart"] = {}

    return session["cart"]


# ==========================================
# VIEW CART
# ==========================================

@cart.route("/cart")
def view_cart():

    cart_data = get_cart()

    products = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_product(int(product_id))

        if not product:
            continue

        subtotal = float(product["price"]) * quantity

        total += subtotal

        products.append({

            "product": product,

            "quantity": quantity,

            "subtotal": subtotal

        })

    return render_template(

        "cart.html",

        cart_items=products,

        total=total,

        format_currency=format_currency

    )


# ==========================================
# ADD TO CART
# ==========================================

@cart.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):

    product = get_product(product_id)

    if not product:

        return redirect(url_for("home"))

    cart = get_cart()

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    session.modified = True

    return redirect(url_for("cart.view_cart"))


# ==========================================
# REMOVE ITEM
# ==========================================

@cart.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):

    cart = get_cart()

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    session.modified = True

    return redirect(url_for("cart.view_cart"))


# ==========================================
# UPDATE QUANTITY
# ==========================================

@cart.route("/cart/update", methods=["POST"])
def update_cart():

    cart = get_cart()

    for product_id in list(cart.keys()):

        quantity = request.form.get(f"qty_{product_id}")

        if quantity:

            quantity = int(quantity)

            if quantity <= 0:

                del cart[product_id]

            else:

                cart[product_id] = quantity

    session.modified = True

    return redirect(url_for("cart.view_cart"))
# ==========================================
# CHECKOUT
# ==========================================

@cart.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart = get_cart()

    if not cart:

        return redirect(url_for("cart.view_cart"))

    products = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_product(int(product_id))

        if not product:
            continue

        subtotal = float(product["price"]) * quantity
        total += subtotal

        products.append({

            "product": product,
            "quantity": quantity,
            "subtotal": subtotal

        })

    if request.method == "POST":

        customer_name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        address = request.form["address"].strip()

        order_id = create_order(

            customer_name,
            phone,
            address,
            total

        )

        for item in products:

            add_order_item(

                order_id,
                item["product"]["id"],
                item["quantity"],
                item["product"]["price"]

            )

        session.pop("cart", None)

        return redirect(

            url_for(
                "cart.order_success",
                order_id=order_id
            )

        )

    return render_template(

        "checkout.html",

        cart_items=products,

        total=total,

        format_currency=format_currency

    )


# ==========================================
# ORDER SUCCESS
# ==========================================

@cart.route("/order/success/<int:order_id>")
def order_success(order_id):

    return render_template(

        "order_success.html",

        order_id=order_id

    )
