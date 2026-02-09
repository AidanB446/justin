
import sqlite3

conn = sqlite3.connect("./orders.db")

cur = conn.cursor()


cur.execute("""
        CREATE TABLE orders (
            ordertype TEXT,
            symbol TEXT,
            qty TEXT,
            side TEXT,
            user TEXT,
            client_order_id TEXT,
            date TEXT
        )
            """)

cur.close()

conn.commit()
conn.close()

