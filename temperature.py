#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sqlite.config import HOST
from sqlite.config import PORT
from sqlite.config import TEMPERATURE_UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_temperature import Temperature

if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    t = Temperature(TEMPERATURE_UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    temperature = t.get_temperature()/100.0
    ts = int(time.time())
    
    with open('/home/pi/Weatherstation/temperature.csv', 'a') as f:
        f.write('{}\t{}\n'.format(ts, temperature))

    ipcon.disconnect()
                                
