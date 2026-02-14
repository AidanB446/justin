
import sqlite3

conn = sqlite3.connect("./master.db")

cur = conn.cursor()

cur.execute("""
            CREATE TABLE master (username TEXT, hash_password TEXT)
            """)

cur.close()

conn.commit()
conn.close()

