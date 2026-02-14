
import sqlite3

conn = sqlite3.connect("./accounts.db")

cur = conn.cursor()

cur.execute("""
    DELETE FROM accounts WHERE name = 'John';
            """)

cur.close()

conn.commit()
conn.close()

