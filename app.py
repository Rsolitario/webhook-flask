from flask import Flask, request, abort
import os, json, requests, urllib.parse
from thefirstock import thefirstock as tf
# install pip install flask[async]
# 9710834326
# RB1096
# Omnamo33@

app = Flask(__name__)
webhook_site = 'https://webhook.site/53aaf13b-194a-4e47-ab25-5f039b30d235'


class Order:
    exchange: str        # NSE / NFO / EEB
    tradingSymbol: str = urllib.parse.quote('')  # NSE NFO
    quantity: str
    price: str
    product: str         # C / M / I C -> Cash and Carry, M -> F&O Normal, I -> Intraday
    transactionType: str  # B / S B -> BUY, S -> SELL
    priceType: str       # LMT / MKT / SL-LMT / SL-MKT
    retention: str       # DAY / EOS / IOC
    triggerPrice: str    # Only to be sent in case of SL / SL-M order
    remarks: str         # User can send remarks for the order


class Login:
    userId: str
    password: str
    TOTP: str
    vendorCode: str
    apiKey: str


async def core(
    data: Order
):
    try:
        PlaceOrder = tf.firstock_placeOrder(
            **data
        )
        if type(PlaceOrder) == type(None):
            abort(401, "Invalid Order")
        return 'success', 200
    except Exception as e:
        abort(400, e)


@app.route("/webhook", methods=['POST'])
async def webhook():
    if request.method == 'POST':
        tmp_data = request.json
        data_stream: Order = tmp_data['Order']
        login_stream: Login = tmp_data['Login']
        try:
            login = tf.firstock_login(
                    **login_stream
                )
            if type(login) == type(None):
                abort(401, "Invalid App Key")
        except Exception as e:
            abort(400, e)
        # print(data, login)
        # print(json.dumps(data))
        requests.post(webhook_site, data=json.dumps(tmp_data),
                      headers={"Content-Type": "application/json"})

        response = await core(data_stream)
        # print(response)
        return response
    else:
        abort(400, "Invalid method")


@app.route("/main")
def home():
    return 'v0.01'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)


'''
{'Order': {
        'exchange': 'Binance',
        'tradingSymbol': 'NSE', 
        'quantity': '100', 
        'price': '5', 
        'product': 'something', 
        'transactionType': 'future', 
        'priceType': 'usd', 
        'retention': 'none', 
        'triggerPrice': '4.5', 
        'remarks': 'something'
    }, 
'Login': {
        'userId': 'alguien', 
        'password': '1234', 
        'TOTP': '123', 
        'vendorCode': '', 
        'apiKey': 'permitido'
    }
}

'''
