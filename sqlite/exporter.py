import time
import sqlite3
import json
import os

from sqlite.config import *


def make_table_entry(connection, dbtable):
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM %s ORDER BY timestamp DESC LIMIT 1" % dbtable)
    current = cursor.fetchone()[0]

    limit = time.time() - (86400 * 2)  # 2 days ago
    cursor.execute("SELECT min(value), max(value) FROM %s WHERE timestamp >= %d" % (dbtable, limit))
    (minvalue, maxvalue) = cursor.fetchone()

    return {
            "current": current,
            "min": minvalue,
            "max": maxvalue
        }


def make_table(conn):
    dict = {}
    for table in SENSORS:
        dict[table] = make_table_entry(conn, table)
    text = json.dumps(dict, separators=(',', ': '))
    with open(OUT_DIR+'/table.json', 'w') as f:
        f.write(text)


def make_series_entry(conn, table):
    cursor = conn.cursor()
    limit = time.time() - (86400 * 2)  # 2 days ago
    cursor.execute("""
     SELECT
       strftime('%Y-%m-%d %H', timestamp, 'unixepoch', 'localtime') as date,
       avg(value)
       FROM """ + table + """
      WHERE timestamp >= """ + str(limit)+ """
   GROUP BY date
   ORDER BY date ASC """)
    result = cursor.fetchall()
    return list(map(lambda x: x[1], result))


def make_series(conn):
    dict = {}
    for table in SENSORS:
        dict[table] = make_series_entry(conn, table)
    text = json.dumps(dict, separators=(',', ': '))
    with open(OUT_DIR+'/series.json', 'w') as f:
        f.write(text)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    connection = sqlite3.connect(SQLITEDB)
    make_table(connection)
    make_series(connection)
    connection.close()

