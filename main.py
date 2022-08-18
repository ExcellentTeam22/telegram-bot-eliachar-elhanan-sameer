import requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
TELEGRAM_INIT_WEBHOOK_URL = "https://api.telegram.org/bot{}/setWebhook?url=https://3321-37-142-167-82.eu.ngrok.io/message".format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

# @app.route('/message', methods=["POST"])
# def handle_message():
#     print("got message")
#     return Response("success")


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    print(chat_id)
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, "Got it"))
    return Response("success")



if __name__ == '__main__':
    app.run(port=5002)







# from flask import Flask
# from flask_ngrok import run_with_ngrok
#
# app = Flask(__name__)
# run_with_ngrok(app)

#
# @app.route("/")
# def hello():
#     return "Hello Geeks!! from Google Colab"
#
#
# if __name__ == "__main__":
#     app.run()