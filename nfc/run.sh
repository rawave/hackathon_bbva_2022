#!/bin/bash
uvicorn main:app --reload --host 0.0.0.0 --ssl-keyfile key.pem --ssl-certfile cert.pem