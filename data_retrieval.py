import sqlite3
conn = sqlite3.connect('cust_satisfaction.db')
cur = conn.cursor()

query = "select * from cust_details;"
cur.execute(query)

for record in cur.fetchall():
    print(record)

cur.close()
conn.close()