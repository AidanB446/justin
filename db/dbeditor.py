
import sqlite3

conn = sqlite3.connect("./accounts.db")

cur = conn.cursor()

cur.execute("""
        CREATE TABLE accounts (
            api_key TEXT,
            api_secret TEXT,
            name TEXT
        )
            """)

cur.close()

conn.commit()
conn.close()

