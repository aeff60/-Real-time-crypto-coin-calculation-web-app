import imp
from urllib3 import response
from flask import *
import json
import os
from urllib.request import urlopen

app = Flask(__name__)

url_api = "https://api.binance.com/api/v1/ticker/price"


@app.route('/')
def home():
    #read data api
    response = urlopen(url_api)

    list_of_symbol = []

    data_json = json.loads(response.read())
    data_list = []
    for i in range(len(data_json)):
        dataprice= data_json[i]['symbol']
        a = dataprice.find("USDT")
        if a != -1:
            data_list.append(data_json[i])
        else:
            pass

    

    for i in range(len(data_json)):
        coin = data_json[i]['symbol']
        list_of_symbol.append(coin)
        coin_USDT = coin.find('USDT')

    print(data_list)

    return render_template('index.html',data = data_json , symbols = list_of_symbol)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))    
    app.run(host='127.0.0.1', port=port, debug=True)