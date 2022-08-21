import requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5465265510:AAHJBqcEvaJ0L7x2y-4P_fOkr_qxxRXrJ2U'
ADDRESS = 'https://1e8e-2a0d-6fc7-330-2de1-99d4-be06-2fac-69be.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/message"
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    bus_line=0
    city=""
    print("got msg")
    chat_id = request.get_json()['message']['chat']['id']
    if request.get_json()['message']['text']:
        bus_line,city = request.get_json()['message']['text'].split(' ')

        print([bus_line,city])
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)