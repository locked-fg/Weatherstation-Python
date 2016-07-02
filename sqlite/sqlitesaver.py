import time
import sqlite3
import os

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_barometer import Barometer
from tinkerforge.bricklet_humidity import Humidity
from tinkerforge.bricklet_temperature import Temperature

from sqlite.config import *


def setup_tables(connection, tablename):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            timestamp INT PRIMARY KEY NOT NULL,
            value REAL NOT NULL
        ) """ % tablename)
    connection.commit()


def insert(connection, table, timestamp, value):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO %s VALUES (%d, %f)" % (table, timestamp, value))
    connection.commit()


def ambient(connection, table):
    ipcon = IPConnection()
    al = AmbientLight(AMBIENT_UID, ipcon)
    ipcon.connect(HOST, PORT)
    value = al.get_illuminance() / 10.0  # Get current illuminance (unit is Lux/10)
    insert(connection, table, time.time(), value)
    ipcon.disconnect()


def barometer(connection, table):
    ipcon = IPConnection()
    b = Barometer(BAROMETER_UID, ipcon)
    ipcon.connect(HOST, PORT)
    value = b.get_air_pressure() / 1000.0  # Get current air pressure (unit is mbar/1000)
    insert(connection, table, time.time(), value)
    ipcon.disconnect()


def humidity(connection, table):
    ipcon = IPConnection()
    h = Humidity(HUMIDITY_UID, ipcon)
    ipcon.connect(HOST, PORT)
    value = h.get_humidity() / 10.0
    insert(connection, table, time.time(), value)
    ipcon.disconnect()


def temperature(connection, table):
    ipcon = IPConnection()
    t = Temperature(TEMPERATURE_UID, ipcon)
    ipcon.connect(HOST, PORT)
    value = t.get_temperature() / 100.0
    insert(connection, table, time.time(), value)
    ipcon.disconnect()


def clean_tables(connection, table):
    ts = time.time() - (86400 * 2)  # 2 days ago
    cursor = connection.cursor()
    cursor.execute("DELETE FROM %s WHERE timestamp < %s" % (table, ts))
    cursor.close()


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    conn = sqlite3.connect(SQLITEDB)

    for table in SENSORS:
        setup_tables(conn, table)
        # clean_tables(conn, table)

    ambient(conn, "ambientlight")
    barometer(conn, "airpressure")
    humidity(conn, "humidity")
    temperature(conn, "temperature")

    conn.close()
