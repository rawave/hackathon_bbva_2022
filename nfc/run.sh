#!/bin/zsh
uvicorn main:app --reload --host 0.0.0.0 --ssl-keyfile decrypted_key.pem --ssl-certfile cert.pem