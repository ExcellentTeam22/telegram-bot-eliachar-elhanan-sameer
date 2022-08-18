import requests
from flask import Flask, Response, request
import math
from collections import Counter

app = Flask(__name__)
dict = {}
popular = [0, 0]
TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
ADDRESS = 'https://f3f9-2-53-16-160.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/message"
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

my_dict_prime = {}

@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got msg")
    # chat_id = request.get_json()['message']['chat']['id']
    if request.get_json()['message']['text']:
        msg_from_usr = request.get_json()['message']['text'].split(' ')
        command = msg_from_usr[0]
        if len(msg_from_usr) == 2:
            num = msg_from_usr[1]
            if command == '/prime':
                handle_prime(num)
            elif command == '/palindrome':
                handle_palindrome(num)
            elif command == '/factorial':
                handle_factorial(num)
            elif command == '/sqrt':
                handle_sqrt(num)
        if command == '/popular':
            handle_popular()


    return Response("success")


@app.route('/factorial', methods=["POST"])
def handle_factorial(num: int):
    chat_id = request.get_json()['message']['chat']['id']
    num = int(num)
    number = 1
    counter = 2
    while number < num:
        number *= counter
        counter += 1
    if number == num & num != 1:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, f"factorial of {counter - 1}"))
    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "not factorial"))


@app.route('/prime', methods=["POST"])
def handle_prime(num: int):
    print("got prime")
    chat_id = request.get_json()['message']['chat']['id']
    num = int(num)

    update_popular(num)
    if num in my_dict_prime.keys():
        my_dict_prime[num] += 1
    else:
        my_dict_prime[num] = 1
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


@app.route('/popular', methods=["POST"])
def handle_popular():
    print("got popular")
    chat_id = request.get_json()['message']['chat']['id']

    if popular[1] != 0:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id,
                                   f"the popular number is {popular[0]} and it appeared {popular[1]} times "))
    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id,
                                   f"there is no popular number yet"))
    return Response("success")


@app.route('/sqrt', methods=["POST"])
def handle_sqrt(num: str):
    chat_id = request.get_json()['message']['chat']['id']
    num = int(num)

    root = math.sqrt(num)
    if int(root + 0.5) ** 2 == num:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "sqrt!"))
    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "Not sqrt!"))

    return Response("success")


def update_popular(number):
    if number in dict:
        dict[number] += 1
    else:
        dict[number] = 1
    if popular[1] < dict[number]:
        popular[0] = number
        popular[1] = dict[number]


def is_prime(num: int):
    for i in range(2, num):
        if (num % i) == 0:
            return False
    return True


@app.route('/palindrome', methods=["POST"])
def handle_palindrome(num: str):
    print("got palindrome")
    chat_id = request.get_json()['message']['chat']['id']
    if is_palindrome(num):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "palindrome"))
    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, "not palindrome"))

    return Response("success")


def is_palindrome(num: str):
    return num == num[::-1]

#
# @app.route('/popular', methods=["POST"])
# def handle_popular():
#     chat_id = request.get_json()['message']['chat']['id']
#     popular_num = 0
#     for key, value in my_dict_prime.items():
#         if value > popular_num:
#             popular_num = key
#
#     res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
#                        .format(TOKEN, chat_id, f"most popular number: {popular_num}"))
#     return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
