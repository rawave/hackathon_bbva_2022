from copyreg import constructor
from tokenize import Name
from urllib import response
from fastapi import Cookie, FastAPI, Response
from fastapi.responses import RedirectResponse
#from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from Classifier import Classifier
from pydantic import BaseModel
from typing import Union
import pandas as pd

app = FastAPI()
clients = pd.read_csv("../files/Clientes_Descriptivo.csv", sep="\t+")
clients_trxs = pd.read_csv("../files/Transacciones_Clientes.csv", sep="\t+")


class NfcData(BaseModel):
    client_id: str


@app.get("/styles.css")
def styles():
    with open("web/styles.css") as cssFile:
        css = cssFile.read()
    return Response(content=css, media_type="text/css", status_code=200)


@app.get("/")
async def login(client_id: Union[str, None] = Cookie(default=None)):
    with open("web/auth.html") as htmlFile:
        html = htmlFile.read()
        if (client_id != None):
            html = html.replace("$client_id", client_id)
        else:
            html = html.replace("$client_id", "")
    return Response(content=html, media_type="text/html", status_code=200)


@app.get("/clientinfo")
async def clientinfo(client_id: Union[str, None] = Cookie(default=None)):
    if (client_id != None):
        with open("web/clientinfo.html") as htmlFile:
            html = htmlFile.read()
            html = addClientInfoHtml(client_id, html)
            return Response(content=html, media_type="text/html", status_code=200)
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
    if (validateClient(data.client_id)):
        response.set_cookie(key="client_id", value=data.client_id)
        return response
    else:
        response.delete_cookie("client_id")
        return response


def addClientInfoHtml(html):
    html = html.replace("$client_info_html", "CLIENT_INFO_HTML")
    return html


@app.post("/nfc/api/v1/identify")
def Identify(data: NfcData):
    # 11DP0KLY  mayor
    # X0FSTCTX  vulnerable
    # 03J6TRTT  discapacitado
    # 60PZ035D  normal
    classifier = Classifier(data.client_id)
    type = classifier.getClassification()
    return {
        "tipo": type,
    }


def validateClient(client_id):
    client = clients.loc[clients["NU_CTE_COD"] == client_id]
    return client.size > 0


def addClientInfoHtml(client_id, html):
    trxs = clients_trxs.loc[clients_trxs["NU_CTE_COD"] == client_id]
    client_info_html = "<table><tr>"
    client_info_html += "<th>Fecha de corte</th>"
    client_info_html += "<th>Fecha de operación</th>"
    client_info_html += "<th>Número de afiliación</th>"
    client_info_html += "<th>Tipo de tarjeta</th>"
    client_info_html += "<th>Importe</th>"
    client_info_html += "</tr>"

    for _, t in trxs.iterrows():
        client_info_html += "<tr>"
        client_info_html += "<td>" + t["FH_CORTE"].format() + "</td>"
        client_info_html += "<td>" + t["FH_OPERACION"] + "</td>"
        client_info_html += "<td>" + str(t["NU_AFILIACION"]) + "</td>"
        client_info_html += "<td>" + t["TIPO_TARJETA"] + "</td>"
        client_info_html += "<td>" + str(t["IM_TRANSACCION"]) + "</td>"
        client_info_html += "</tr>"

    client_info_html += "</table>"
    html = html.replace("$client_info_html", client_info_html)
    # print(html)
    return html
