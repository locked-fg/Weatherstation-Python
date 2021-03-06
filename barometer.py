#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sqlite.config import HOST
from sqlite.config import PORT
from sqlite.config import BAROMETER_UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_barometer import Barometer

if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    b = Barometer(BAROMETER_UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    # Get current air pressure (unit is mbar/1000)
    air_pressure = b.get_air_pressure() /1000.0

    #print('Air Pressure: ' + str(air_pressure) + ' mbar')

    # Get current altitude (unit is cm)
    altitude = b.get_altitude()/100.0

    ts = int(time.time())
    
    with open('/home/pi/Weatherstation/barometer.csv', 'a') as f:
        f.write('{}\t{}\n'.format(ts, air_pressure))

    ipcon.disconnect()
                                
