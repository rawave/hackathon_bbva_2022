from copyreg import constructor
from tokenize import Name
from urllib import response
from fastapi import Cookie, FastAPI, Response
from fastapi.responses import RedirectResponse
#from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class NfcData(BaseModel):
    client_id: str


class ClientInfo(BaseModel):
    client_id: str
    name: str


@app.get("/")
async def login():
    with open("web/auth.html") as htmlFile:
        data = htmlFile.read()
    return Response(content=data, media_type="text/html", status_code=200)


@app.get("/clientinfo")
async def clientinfo(client_id: Union[str, None] = Cookie(default=None)):
    if (client_id != None):
        with open("web/clientinfo.html") as htmlFile:
            html = htmlFile.read()
            return Response(content=addClientInfoHtml(html), media_type="text/html", status_code=200)
    else:
        return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("client_id")
    return response


@app.post("/nfc/api/v1/senddata")
def api_send(data: NfcData):
    print(data)
    response = Response(content="OK", status_code=200)
    response.set_cookie(key="client_id", value=data.client_id)
    return response

def addClientInfoHtml(html):
    html = html.replace("$client_info_html","CLIENT_INFO_HTML")
    return html