import os
from flask import *  
import json
from urllib.request import urlopen

from numpy import double, float64
app  = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  
def home():

    global symbol_dropdown_str, balance_str
    totalprice = ""

    #ที่อยู่ของ API
    url = "https://api.binance.com/api/v1/ticker/price"
    
    #class 'http.client.HTTPResponse'
    response = urlopen(url)
    data = json.loads(response.read())

    data_onlyusdt = []

    #สร้างลูปสำหรับเอาเฉพาะตัวย่อของการแลกเปลี่ยนเงิน
    for i in range(len(data)):
        symbol= data[i]['symbol']# ['symbol'] คือ key ที่อยู่ใน API
        findusdt = symbol.find("USDT") #หาว่าใน key ที่ชื่อ symbol มีตัวอักษร usdt หรือไม่
        if findusdt != -1: #ถ้าเจอค่าจะไม่เท่ากับ -1
            data_onlyusdt.append(data[i]) #เอาข้อมูลที่ symbol มีคำว่า usdt เก็บไว้ใน list ชื่อ data_onlyusdt
        else:
            pass


    #แยกข้อมูลของแต่ละ key ไว้ใน list เดียวกัน
    symbol_usdt_lsit = []
    price_usdt_lsit = []

    for j in range(len(data_onlyusdt)):
        symbol_onlyusdt = data_onlyusdt[j]['symbol']
        price_onlyusdt = data_onlyusdt[j]['price']
        symbol_usdt_lsit.append(symbol_onlyusdt)
        price_usdt_lsit.append(price_onlyusdt)
        
    #เริ่มต้นใช้ Cookie    
    listCookie = []
    totalUsdt = 0.0


    if request.method == "POST": 
         #รับค่าจากฟอร์มที่ชื่อว่า symbol
         symbol_dropdown = request.form.get('coin')
         symbol_dropdown_str = str(symbol_dropdown) 
     
         balance = request.form.get('balance') 
         balance_str = str(balance)
        
         for k in range(len(symbol_usdt_lsit)):
            symbol_selected = symbol_usdt_lsit[k]
            prince_current = price_usdt_lsit[k]
            check_symbol_selected = symbol_selected.find(symbol_dropdown_str)
            if check_symbol_selected != -1:
                price = prince_current    
            else:
                pass

         listCookie = json.loads(request.cookies.get('symbol'))
         for item in listCookie:
             totalUsdt = totalUsdt + item[2]

         totalprice = double(balance_str) * double(price)
         listCookie.append([symbol_dropdown_str, balance_str, totalprice])
                
    else:
        symbol_dropdown_str = " "
        balance_str = "0"
        
    resp = make_response(render_template('home.html',total = totalUsdt, mycoin=listCookie, data=symbol_usdt_lsit, coinsymbol=symbol_dropdown_str, valuebalance=balance_str))
    resp.set_cookie('symbol',json.dumps(listCookie)) 
    return resp
      
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)