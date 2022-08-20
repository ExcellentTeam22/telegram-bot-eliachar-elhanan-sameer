import time

import requests
from flask import Flask, Response, request, redirect, url_for
import datetime
from location import Location
from convert_to_coords import get_coords_lon_lat

app = Flask(__name__)
app.config["DEBUG"] = True

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
ADDRESS = 'https://3867-2a10-8012-f-7660-a445-1531-de61-7f9a.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/"

requests.get(TELEGRAM_INIT_WEBHOOK_URL)


def send_message(text):
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")


def get_message():
    return request.get_json()['message']['text'].split(' ')


def respond_message(prefix, current, flag=False):
    print(f"{prefix}: {current}")
    text = f"{prefix}: {current}"
    send_message(text)
    if flag:
        text = "Enter your destination (street, city, country and region(IL/EU/US/AU)) seperated by space:"
        send_message(text)


def handle_input(*args, flag=True):
    answer = get_message()

    if len(answer) == 4:
        location = Location(street=answer[0], city=answer[1], country=answer[2], region=answer[3])

        respond_message(args[0], location.street)
        respond_message(args[1], location.city)
        respond_message(args[2], location.country)
        respond_message(args[3], location.region, flag=flag)

        return location
        # if flag:
        #     requests.get(TELEGRAM_INIT_WEBHOOK_URL + 'destination')
            # destination()
            # return redirect(url_for('destination'))
    else:
        err_msg = "Your answer is incorrect format\n" \
                  "Please enter your street, city, country and region(IL/EU/US/AU) seperated by space"
        send_message(err_msg)


@app.route('/', methods=["POST"])
def start():
    print("start")
    # send_message("Enter your country, city and street seperated by space:")
    # time.sleep(1)
    src_location = handle_input("Your src street is", "Your src city source is", "Yur src country is",
                                "Your src region is:", flag=True)
    print(src_location)

    lat, lon = get_coords_lon_lat(src_location)
    src_location.add_coords(lat, lon)
    print(src_location)

    send_message(str(src_location))

    return Response("success")


@app.route('/destination', methods=["POST"])
def destination():
    print("dest")

    handle_input("Your dest street is", "Your dest city source is", "Your dest country is",
                 "Your dest region is", flag=False)

    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)


# Agripas Jerusalem Israel IL
# Ofira Jerusalem Israel IL
# Shoham Jerusalem Israel IL
# Dizengoff Tel Aviv Israel IL
# Dizengoff Tel-Aviv Israel IL
# arlozorov Tel-Aviv Israel IL
# Crimee Paris France EU
# shor eilat israel IL
# tsahal haifa israel IL

