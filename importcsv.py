import sqlite3
import os
import csv
from sqlite.config import *


def mycsv_reader(csv_reader):
    while True:
        try:
            yield next(csv_reader)
        except csv.Error:
            # error handling what you want.
            pass
        continue
    return


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    conn = sqlite3.connect(SQLITEDB)
    cursor = conn.cursor()

    tables = ["ambientlight", "airpressure", "humidity", "temperature"]
    csvs = ["ambientlight.csv", "barometer.csv", "humidity.csv", "temperature.csv"]

    for i in range(0, len(tables)):
        print("processing " + csvs[i])
        reader = mycsv_reader(csv.reader(open(csvs[i], 'rU'), delimiter='\t'))
        counter = 0
        for row in reader:
            counter += 1
            cursor.execute("""INSERT OR IGNORE INTO %s VALUES (%d, %f)""" % (tables[i], int(row[0]), float(row[1])))
            if counter % 50000 == 0:
                print("table %s, line %d" % (tables[i], counter))
                conn.commit()
        conn.commit()
