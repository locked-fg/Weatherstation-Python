#!/bin/bash

export PYTHONPATH="$HOME/Weatherstation"
cd $HOME/Weatherstation
python3 ./sqlite/sqlitesaver.py
python3 ./sqlite/exporter.py
