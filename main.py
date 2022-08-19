import time

import requests
from flask import Flask, Response, request, redirect, url_for
import datetime

app = Flask(__name__)

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
ADDRESS = 'https://3867-2a10-8012-f-7660-a445-1531-de61-7f9a.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/"

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


def send_message(text):
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")
    # print(res.text)


def get_message():
    return request.get_json()['message']['text'].split()


def country_handle(prefix, country):
    print(f"{prefix}: {country}")
    text = f"{prefix}: {country}"
    send_message(text)


def city_handle(prefix, city):
    print(f"{prefix}: {city}")
    text = f"{prefix}: {city}"
    send_message(text)


def street_handle(prefix, street, flag=True):
    print(f"{prefix}: {street}")
    text = f"{prefix}: {street}"
    send_message(text)

    if flag:
        text = "Enter your destination (country, city and street) seperated by space:"
        send_message(text)


def handle_input(*args, flag=True):
    answer = get_message()

    print(f"flag: {flag}")

    if len(answer) == 3:
        country_handle(args[0], answer[0])
        city_handle(args[1], answer[1])
        street_handle(args[2], answer[2], flag=flag)
        if flag:
            requests.get(TELEGRAM_INIT_WEBHOOK_URL + 'destination')
            # destination()
        # return redirect(url_for('destination')) if flag else 0
    else:
        err_msg = "Your answer is incorrect format\n" \
                  "Please enter your country, city and street seperated by space"
        send_message(err_msg)


@app.route('/', methods=["POST"])
def start():
    print("start")
    # send_message("Enter your country, city and street seperated by space:")
    # time.sleep(1)
    handle_input("Your source country is", "Your source city source is", "Yur source street is", flag=True)

    return Response("success")


@app.route('/destination', methods=["POST"])
def destination():
    print("dest")

    # data = await async_db_query(...)

    handle_input("Your dest country is", "Your dest city source is", "Your dest street is", flag=False)

    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)