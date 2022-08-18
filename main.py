import requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
TELEGRAM_INIT_WEBHOOK_URL = "https://api.telegram.org/bot{}/setWebhook?url=https://7b52-82-80-173-170.eu.ngrok.io/message".format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    print(request.get_json()['message']['text'])
    msg_from_usr = request.get_json()['message']['text'].split(' ')
    if msg_from_usr[0] == '/prime':
        handle_prime(msg_from_usr[1])

    return Response("success")


@app.route('/prime', methods=["POST"])
def handle_prime(num: int):
    print("got prim")
    chat_id = request.get_json()['message']['chat']['id']
    num = int(num)
    if num % 2 == 0:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "Come on dude, you know even numbers are not prime!"))
    elif is_prime(num):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "prime"))
    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "not prime"))
    return Response("success")


def is_prime(num: int):
    for i in range(2, num):
        if (num % i) == 0:
            return False
    return True


if __name__ == '__main__':
    app.run(port=5002)

