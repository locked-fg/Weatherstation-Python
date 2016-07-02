#!/bin/bash

export PYTHONPATH="$HOME/wetterstation"
cd $HOME/wetterstation
python3 ./sqlite/sqlitesaver.py
python3 ./sqlite/exporter.py
