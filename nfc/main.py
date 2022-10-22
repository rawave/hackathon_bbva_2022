from tokenize import Name
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
    return getClientData(data)

def getClientData(data: NfcData):
    # TODO: Validate client in db
    # TODO: Get client info
    client_info = ClientInfo(name="Faus")
    return client_info