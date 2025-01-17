#!/bin/bash

export PYTHONPATH="$HOME/Weatherstation"
cd $HOME/Weatherstation
~/venv/bin/python3 ./sqlite/sqlitesaver.py
~/venv/bin/python3 ./sqlite/exporter.py
