#!/bin/bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m flask --app main run --host 0.0.0.0 --port 5000