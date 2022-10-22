#!/bin/bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --ssl-keyfile decrypted_key.pem --ssl-certfile cert.pem