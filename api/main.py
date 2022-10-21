from flask import Flask, render_template
from icecream import ic
app = Flask(__name__)

@app.route("/identify/<client>", methods=['GET'])
def Identify(client):
    ic(client)
    return {
        "tipo": "vulnerable",
    }

@app.route("/auth", methods=['GET'])
def Auth():
    return render_template('user.html.jinja', name="User")