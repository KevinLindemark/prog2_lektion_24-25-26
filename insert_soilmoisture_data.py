from random import randint
import sqlite3 as lite
from time import sleep
con = lite.connect('database.sqlite')
"""
CREATE TABLE soilmoisture (timestamp DATETIME,  moisture REAL);
/* No STAT tables available */
"""
def insert_moisture_data(moisture):
    query = "INSERT INTO soilmoisture (timestamp, moisture) VALUES(datetime('now'), ?)"
    data = (float(moisture),)
    print(type(data), data)
    with con:
        cur = con.cursor() 
        cur.execute(query, data)
