from config import Config
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db():
    """
    Returns a PostgreSQL connection.
    """

    return psycopg2.connect(
        Config.DATABASE_URL,
        cursor_factory=RealDictCursor
    )


def init_db():
    """
    Creates all database tables.
    """

    conn = get_db()
    cur = conn.cursor()

    # USERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # CATEGORIES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    # PRODUCTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price NUMERIC(10,2) NOT NULL,
            image TEXT,
            category_id INTEGER REFERENCES categories(id),
            stock INTEGER DEFAULT 0,
            featured BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ORDERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100),
            phone VARCHAR(30),
            address TEXT,
            total NUMERIC(10,2),
            status VARCHAR(30) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ORDER ITEMS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items(
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER,
            price NUMERIC(10,2)
        )
    """)

    # LOGIN ATTEMPTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts(
            ip VARCHAR(100) PRIMARY KEY,
            attempts INTEGER DEFAULT 0,
            lockout_until TIMESTAMP
        )
    """)

    conn.commit()

    cur.close()
    conn.close()