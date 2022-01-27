import datetime
import sqlite3
from os import environ
from time import sleep

import telebot

TOKEN = environ['TELEBOT_TOKEN']
bot = telebot.TeleBot(TOKEN)
connection = sqlite3.connect(f'../{environ["PROJECT_FOLDER"]}/todo/db.sqlite3')
cursor = connection.cursor()
last_function = f'"{datetime.datetime.utcnow() - datetime.timedelta(days=1)}"'


def get_telegram_and_user_id_list():
    telegram_list = list(cursor.execute('SELECT telegram_id, usr_id from todo_app_account'))
    return telegram_list


def get_messages(user_id):
    present_time = f'"{datetime.datetime.utcnow()}"'
    messages_request = 'SELECT text FROM todo_app_message WHERE account_id = ? AND message_date BETWEEN ? AND ?'
    param_for_messages = (str(user_id), last_function, present_time)
    messages = list(cursor.execute(messages_request, param_for_messages))
    if messages:
        return messages
    else:
        return None


def main_function():
    telegram_and_user_id_list = get_telegram_and_user_id_list()
    for telegram_and_user_id in telegram_and_user_id_list:
        telegram_id, user_id = list(telegram_and_user_id)
        messages = get_messages(user_id)
        if messages:
            for message_ in messages:
                try:
                    bot.send_message(telegram_id, f'you have new message: {message_[0]}')
                except:
                    continue


while True:
    sleep(3)
    main_function()
    last_function = f'"{datetime.datetime.utcnow()}"'
