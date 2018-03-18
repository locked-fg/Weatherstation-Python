# Project for polling the sensor data.

Data is written to CSVs and into an SQLite DB.
48h data is being exported to JSON which is used in the [web frontend](https://github.com/locked-fg/Weatherstation-web).

# Install
Install Pyton and dependencies
```
sudo apt install python3 sqlite python3-setuptools
sudo easy_install3 pip
pip install tinkerforge
```
Download weatherstation
```
cd /home/pi
git clone https://github.com/locked-fg/Weatherstation-Python.git Weatherstation
```

Optional: Restore data at `~/Weatherstation/sqlite/sensors.db` 

Add entries to crontab 
```
* * * * * ~/Weatherstation/temperature.py
* * * * * ~/Weatherstation/humidity.py
* * * * * ~/Weatherstation/ambientlight.py
* * * * * ~/Weatherstation/barometer.py
* * * * * ~/Weatherstation/startSqlite.sh
* * * * * curl -T ~/Weatherstation/data/series.json ftp://[hostname] --user ftplogin:password
* * * * * curl -T ~/Weatherstation/data/table.json  ftp://[hostname] --user ftplogin:password
```