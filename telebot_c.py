import time
import datetime

import telebot
import sqlite3

TOKEN = '5132273473:AAEkJ6BWsVUXjpp5o8mfRqGnp1AsnYSBluk'
bot = telebot.TeleBot(TOKEN)
last_function = datetime.datetime.now() - datetime.timedelta(days=1)
connection = sqlite3.connect('../todo_app/todo/db.sqlite3')
cursor = connection.cursor()


def get_telegram_and_user_id_list():
    telegram_list = list(cursor.execute(f'SELECT telegram_id, usr_id from todo_app_account'))
    return telegram_list


def get_messages(user_id):
    messages = list(cursor.execute(f'SELECT text FROM todo_app_message WHERE account_id = {user_id} AND '
                                   f'message_date BETWEEN "{last_function}" '
                                   f'AND "{datetime.datetime.now()-datetime.timedelta(hours=2)}"'))
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
    time.sleep(10)
    main_function()
    last_function = datetime.datetime.now() - datetime.timedelta(hours=2)
