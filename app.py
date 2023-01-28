from flask import Flask, request, abort
import os
app = Flask(__name__)

@app.route("/ebhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)

@app.route("/main")
def home():
    return 'hola mundo'

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))