from database import get_db


# =====================================================
# USERS
# =====================================================

def create_user(name, email, password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users(
            name,
            email,
            password
        )
        VALUES(%s,%s,%s)
    """, (
        name,
        email,
        password
    ))

    conn.commit()

    cur.close()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM users
        WHERE email=%s
    """, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


def get_user_by_id(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM users
        WHERE id=%s
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


def total_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """)

    total = cur.fetchone()["total"]

    cur.close()
    conn.close()

    return total


# =====================================================
# CATEGORIES
# =====================================================

def get_categories():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM categories
        ORDER BY name
    """)

    categories = cur.fetchall()

    cur.close()
    conn.close()

    return categories


def get_category(category_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM categories
        WHERE id=%s
    """, (category_id,))

    category = cur.fetchone()

    cur.close()
    conn.close()

    return category


# =====================================================
# PRODUCTS
# =====================================================

def get_products():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.*,
            c.name AS category_name
        FROM products p
        LEFT JOIN categories c
        ON c.id=p.category_id
        ORDER BY p.created_at DESC
    """)

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products


def get_featured_products():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.*,
            c.name AS category_name
        FROM products p
        LEFT JOIN categories c
        ON c.id=p.category_id
        WHERE featured=TRUE
        ORDER BY created_at DESC
    """)

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products


def get_product(product_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.*,
            c.name AS category_name
        FROM products p
        LEFT JOIN categories c
        ON c.id=p.category_id
        WHERE p.id=%s
    """, (product_id,))

    product = cur.fetchone()

    cur.close()
    conn.close()

    return product


def search_products(search):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.*,
            c.name AS category_name
        FROM products p
        LEFT JOIN categories c
        ON c.id=p.category_id
        WHERE LOWER(p.name)
        LIKE LOWER(%s)
        ORDER BY p.created_at DESC
    """, (f"%{search}%",))

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products


def get_products_by_category(category_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.*,
            c.name AS category_name
        FROM products p
        LEFT JOIN categories c
        ON c.id=p.category_id
        WHERE category_id=%s
        ORDER BY p.created_at DESC
    """, (category_id,))

    products = cur.fetchall()

    cur.close()
    conn.close()

    return products


def create_product(
    name,
    description,
    price,
    image,
    category_id,
    stock,
    featured
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products(
            name,
            description,
            price,
            image,
            category_id,
            stock,
            featured
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s)
    """, (
        name,
        description,
        price,
        image,
        category_id,
        stock,
        featured
    ))

    conn.commit()

    cur.close()
    conn.close()


def update_product(
    product_id,
    name,
    description,
    price,
    image,
    category_id,
    stock,
    featured
):
    conn = get_db()
    cur = conn.cursor()

    if image:

        cur.execute("""
            UPDATE products
            SET
                name=%s,
                description=%s,
                price=%s,
                image=%s,
                category_id=%s,
                stock=%s,
                featured=%s
            WHERE id=%s
        """, (
            name,
            description,
            price,
            image,
            category_id,
            stock,
            featured,
            product_id
        ))

    else:

        cur.execute("""
            UPDATE products
            SET
                name=%s,
                description=%s,
                price=%s,
                category_id=%s,
                stock=%s,
                featured=%s
            WHERE id=%s
        """, (
            name,
            description,
            price,
            category_id,
            stock,
            featured,
            product_id
        ))

    conn.commit()

    cur.close()
    conn.close()


def delete_product(product_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM products
        WHERE id=%s
    """, (product_id,))

    conn.commit()

    cur.close()
    conn.close()


def total_products():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM products
    """)

    total = cur.fetchone()["total"]

    cur.close()
    conn.close()

    return total


# =====================================================
# ORDERS
# =====================================================

def create_order(customer_name, phone, address, total):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders(
            customer_name,
            phone,
            address,
            total
        )
        VALUES(%s,%s,%s,%s)
        RETURNING id
    """, (
        customer_name,
        phone,
        address,
        total
    ))

    order_id = cur.fetchone()["id"]

    conn.commit()

    cur.close()
    conn.close()

    return order_id


def add_order_item(order_id, product_id, quantity, price):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO order_items(
            order_id,
            product_id,
            quantity,
            price
        )
        VALUES(%s,%s,%s,%s)
    """, (
        order_id,
        product_id,
        quantity,
        price
    ))

    conn.commit()

    cur.close()
    conn.close()


def get_orders():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM orders
        ORDER BY created_at DESC
    """)

    orders = cur.fetchall()

    cur.close()
    conn.close()

    return orders


def update_order_status(order_id, status):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status=%s
        WHERE id=%s
    """, (
        status,
        order_id
    ))

    conn.commit()

    cur.close()
    conn.close()


def total_orders():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM orders
    """)

    total = cur.fetchone()["total"]

    cur.close()
    conn.close()

    return total


def total_revenue():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(total),0) AS revenue
        FROM orders
    """)

    revenue = cur.fetchone()["revenue"]

    cur.close()
    conn.close()

    return revenue


# =====================================================
# LOGIN ATTEMPTS
# =====================================================

def get_login_attempt(ip):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM login_attempts
        WHERE ip=%s
    """, (ip,))

    attempt = cur.fetchone()

    cur.close()
    conn.close()

    return attempt


def save_login_attempt(ip, attempts, lockout_until):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO login_attempts(
            ip,
            attempts,
            lockout_until
        )
        VALUES(%s,%s,%s)
        ON CONFLICT(ip)
        DO UPDATE SET
            attempts=EXCLUDED.attempts,
            lockout_until=EXCLUDED.lockout_until
    """, (
        ip,
        attempts,
        lockout_until
    ))

    conn.commit()

    cur.close()
    conn.close()


def clear_login_attempt(ip):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM login_attempts
        WHERE ip=%s
    """, (ip,))

    conn.commit()

    cur.close()
    conn.close()