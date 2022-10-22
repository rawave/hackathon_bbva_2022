from fastapi import FastAPI, Response
#from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/nfc")
async def main():
    with open("web/auth.html") as htmlFile:
        data = htmlFile.read()
    return Response(content=data, media_type="text/html", status_code=200)