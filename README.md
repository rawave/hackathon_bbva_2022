# README

## Run project

```
cd nfc
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile decrypted_key.pem --ssl-certfile cert.pem
```