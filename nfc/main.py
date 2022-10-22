from urllib import response
from fastapi import FastAPI, Response
#from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class NfcData(BaseModel):
    client_id: str

class ClientInfo(BaseModel):
    name: str

@app.get("/nfc")
async def root():
    with open("web/auth.html") as htmlFile:
        data = htmlFile.read()
    return Response(content=data, media_type="text/html", status_code=200)

@app.post("/nfc/api/v1/senddata")
def api_send(data: NfcData):
    response = ClientInfo(name="Faus")
    return response