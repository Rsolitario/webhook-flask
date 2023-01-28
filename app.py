from flask import Flask, request, abort
import os
import json
app = Flask(__name__)

webhook_site = 'https://webhook.site/53aaf13b-194a-4e47-ab25-5f039b30d235'


@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        request.post(webhook_site, data=json.dumps(data),
                     headers={'Content-Type: application/json'})
        return 'success', 200
    else:
        abort(400)


@app.route("/main")
def home():
    return 'hola mundo'

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
