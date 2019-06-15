import time
import sqlite3
import json
import os

from sqlite.config import *
from datetime import datetime, timedelta


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
      WHERE timestamp >= """ + str(limit) + """
   GROUP BY date """)
    result = cursor.fetchall()
    return fill_gaps(result)


def fill_gaps(tuples):
    """
    creates a list that has values for the last 48 hours and replaces missing values with a default value
    :param tuples: the cursor (date time string, value)
    :return: list of values
    """
    current_dict = {date_string: value for date_string, value in tuples}
    expected_keys = map(lambda x: (datetime.now() - timedelta(hours=x)).strftime("%Y-%m-%d %H"), reversed(range(0, 48)))
    return list(map(lambda x: current_dict.get(x, 1), expected_keys))


def make_series(conn):
    result_dict = {table: make_series_entry(conn, table) for table in SENSORS}
    text = json.dumps(result_dict, separators=(',', ': '))
    with open(OUT_DIR+'/series.json', 'w') as f:
        f.write(text)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    connection = sqlite3.connect(SQLITEDB)
    make_table(connection)
    make_series(connection)
    connection.close()

