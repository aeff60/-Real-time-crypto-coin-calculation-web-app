# import imp
from urllib import response
from flask import *
import json
import os
from urllib.request import urlopen

app = Flask(__name__)

url_api = "https://api.binance.com/api/v1/ticker/price"


@app.route('/')
def home():

    #read data api
    url_api = "0.0.0.0"
    response = urlopen(url_api)
    data_json = json.loads(response.read())

    return render_template('index.html',data = data_json)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))    