import requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
ADDRESS = 'https://f080-2a10-8012-f-7660-a445-1531-de61-7f9a.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/message"
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got msg")
    chat_id = request.get_json()['message']['chat']['id']
    if request.get_json()['message']['text']:
        msg_from_usr = request.get_json()['message']['text'].split(' ')

    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)