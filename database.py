# creating database and table using sqlite3

import sqlite3
conn = sqlite3.connect('cust_satisfaction.db')   # database creation
cur = conn.cursor()

# table creation
query_to_create_table = """                     
    create table cust_details(
        age int,
        flight_distance int,
        inflight_entertainment int,
        baggage_handling int,
        cleanliness int,
        departure_delay int,
        arrival_delay int,

        gender varchar (10),
        customer_type varchar (15),
        travel_type varchar (15),
        class_type varchar (20),
        prediction varchar (15)
    )
"""

cur.execute(query_to_create_table)
print('YOUR DATABASE AND TABLE IS CREATED...')
cur.close()
conn.close()