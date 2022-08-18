import requests
from flask import Flask, Response, request
import math
from collections import Counter

app = Flask(__name__)

TOKEN = '5661110898:AAH9WEsgFUSx7bLKQBtIcs4lHuw6aEbTSw0'
ADDRESS = 'https://f080-2a10-8012-f-7660-a445-1531-de61-7f9a.eu.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={ADDRESS}/message"
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

popular = [0, 0]
my_dict_prime = {}


def is_palindrome(num: str):
    return num == num[::-1]


def is_prime(num: int):
    for i in range(2, num):
        if (num % i) == 0:
            return False
    return True


def update_popular(number):
    if number in my_dict_prime:
        my_dict_prime[number] += 1
    else:
        my_dict_prime[number] = 1
    if popular[1] < my_dict_prime[number]:
        popular[0] = number
        popular[1] = my_dict_prime[number]


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


if __name__ == '__main__':
    app.run(port=5002)
