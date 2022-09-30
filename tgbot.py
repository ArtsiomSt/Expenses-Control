import telebot
import requests
from telebot import types

domen = 'http://127.0.0.1:8000/'

botsite = telebot.TeleBot('5337259262:AAGgF5IkIBs91MU3lvPw_g8af-9WeTS7-xg')

@botsite.message_handler(commands=['start'])
def start(message):
    message_for_user = f'Hello {message.from_user.username}, type /help to get list of commands'
    # buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # link_account = types.KeyboardButton('/linkaccount')
    # buttons.add(link_account)
    botsite.send_message(message.chat.id, message_for_user)


@botsite.message_handler(commands=['help'])
def help(message):
    botsite.send_message(message.chat.id, message)
    message_for_user = 'Here is the list of commands /linkaccount'
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    link_account = types.KeyboardButton('/linkaccount')
    buttons.add(link_account)
    botsite.send_message(message.chat.id, message_for_user, reply_markup=buttons)


@botsite.message_handler(commands=['linkaccount'])
def linkaccountstart(message):
    msg = botsite.send_message(message.chat.id, 'Do you have an account on our site?')
    botsite.register_next_step_handler(msg, get_answer)


def get_answer(message):
    text_from_user = message.text
    if text_from_user.lower() != 'yes':
        botsite.send_message(message.chat.id, 'Dismissed')
        return
    msg = botsite.send_message(message.chat.id, 'Send your Username And Password in form Username/Password')
    botsite.register_next_step_handler(msg, get_username)


def get_username(message):
    username_and_pass_from_user = message.text
    u_p = username_and_pass_from_user.split('/')
    if not len(u_p) == 2:
        botsite.send_message(message.chat.id, 'Unable to link, try again')
        return
    for_req = {
        "username": u_p[0],
        "password": u_p[1],
    }
    url_log = 'auth/token/login'
    url = domen+url_log
    resp = requests.post(url, json=for_req)
    if not 'auth_token' in resp.json().keys():
        botsite.send_message(message.chat.id, 'Unable to link with those creditials')
        return
    for_creating_link = {
        "username" : u_p[0],
        "usertgid": message.from_user.id
    }
    url_create = 'api/v1/linktg'
    url = domen+url_create
    resp_1 = requests.post(url, data=for_creating_link)
    botsite.send_message(message.chat.id, 'Linked')


@botsite.message_handler(commands=['myspents'])
def get_self_spents(message):
    url = domen+'api/v1/getusersspents/'
    resp = requests.get(url, params={'usertgid': message.from_user.id})
    url = domen+'api/v1/getuserscats/'
    resp_cats = requests.get(url, params={'usertgid': message.from_user.id})
    print(resp_cats.json())
    print(resp.json())
    for item in resp.json()['spents']:
        message_for_user = ''
        title = item['title']
        all_spents = item['amount']*item['price_for_unit']
        cat_pk = item['category']
        for item in resp_cats.json():
            if cat_pk == item['pk']:
                cat_title = item['title']
        message_for_user += f'Name of spending: {title} \n'
        message_for_user +=f'Spent: {all_spents} \n'
        message_for_user += f'Category: {cat_title}'
        botsite.send_message(message.chat.id, message_for_user)



botsite.polling(none_stop=True)
