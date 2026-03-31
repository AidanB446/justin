

import sqlite3

conn = sqlite3.connect("./orders.db")

cur = conn.cursor()

cur.execute("""

        DELETE FROM orders 

            """)

cur.close()

conn.commit()
conn.close()

conn = sqlite3.connect("./accounts.db")

cur = conn.cursor()

cur.execute("""
        DELETE FROM accounts 
            """)

cur.close()

conn.commit()
conn.close()


