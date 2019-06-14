#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sqlite.config import HOST
from sqlite.config import PORT
from sqlite.config import AMBIENT_UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight

if __name__ == "__main__":
    ipcon = IPConnection()  # Create IP connection
    al = AmbientLight(AMBIENT_UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    # Get current illuminance (unit is Lux/10)
    illuminance = al.get_illuminance() /10.0
    
    ts = int(time.time())
    
    with open('/home/pi/Weatherstation/ambientlight.csv', 'a') as f:
        f.write('{}\t{}\n'.format(ts, illuminance))

    ipcon.disconnect()
                                
