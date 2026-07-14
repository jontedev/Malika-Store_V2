from database import get_db


def seed_categories():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM categories")
    total = cur.fetchone()["total"]

    if total == 0:

        categories = [

            ("Phones",),
            ("Laptops",),
            ("Accessories",),
            ("Audio",),
            ("Wearables",)

        ]

        cur.executemany(
            "INSERT INTO categories(name) VALUES(%s)",
            categories
        )

        conn.commit()

    cur.close()
    conn.close()


def seed_products():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM products")
    total = cur.fetchone()["total"]

    if total > 0:

        cur.close()
        conn.close()
        return

    cur.execute("SELECT id,name FROM categories")
    categories = {
        row["name"]: row["id"]
        for row in cur.fetchall()
    }

    products = [

        (
            "Samsung Galaxy S24",
            "Samsung flagship smartphone.",
            89999,
            None,
            categories["Phones"],
            15,
            True
        ),

        (
            "iPhone 15",
            "Apple smartphone.",
            109999,
            None,
            categories["Phones"],
            12,
            True
        ),

        (
            "Dell Inspiron 15",
            "15 inch laptop.",
            68999,
            None,
            categories["Laptops"],
            8,
            False
        ),

        (
            "HP EliteBook 840",
            "Business laptop.",
            79999,
            None,
            categories["Laptops"],
            5,
            True
        ),

        (
            "Sony WH-1000XM5",
            "Noise cancelling headphones.",
            42999,
            None,
            categories["Audio"],
            20,
            False
        ),

        (
            "JBL Flip 6",
            "Portable Bluetooth speaker.",
            16999,
            None,
            categories["Audio"],
            25,
            False
        ),

        (
            "Apple Watch Series 9",
            "Premium smartwatch.",
            55999,
            None,
            categories["Wearables"],
            10,
            True
        ),

        (
            "Logitech G502",
            "Gaming mouse.",
            5999,
            None,
            categories["Accessories"],
            40,
            False
        ),

        (
            "Redragon K552",
            "Mechanical keyboard.",
            4999,
            None,
            categories["Accessories"],
            30,
            False
        ),

        (
            "Anker Power Bank 20000mAh",
            "Fast charging power bank.",
            6499,
            None,
            categories["Accessories"],
            18,
            False
        )

    ]

    cur.executemany("""
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
    """, products)

    conn.commit()

    cur.close()
    conn.close()