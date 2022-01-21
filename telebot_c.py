import time
import datetime

import telebot
import sqlite3

TOKEN = '5132273473:AAEkJ6BWsVUXjpp5o8mfRqGnp1AsnYSBluk'
bot = telebot.TeleBot(TOKEN)
last_function = datetime.datetime.now() - datetime.timedelta(days=1)


def get_telegram_and_user_id_list(cursor):
    telegram_list = list(cursor.execute(f'SELECT telegram_id, usr_id from todo_app_account'))
    return telegram_list


def get_messages(user_id, cursor):
    messages = list(cursor.execute(f'SELECT text FROM todo_app_message WHERE account_id = {user_id} AND '
                                   f'message_date BETWEEN "{last_function}" '
                                   f'AND "{datetime.datetime.now()-datetime.timedelta(hours=2)}"'))
    print(last_function, datetime.datetime.now())
    if messages:
        return messages[0]
    else:
        return None


def main_function():
    connection = sqlite3.connect('../todo/todo_app/todo/db.sqlite3')
    cursor = connection.cursor()
    telegram_and_user_id_list = get_telegram_and_user_id_list(cursor)
    for telegram_and_user_id in telegram_and_user_id_list:
        print(telegram_and_user_id)
        telegram_id, user_id = list(telegram_and_user_id)
        messages = get_messages(user_id, cursor)
        if messages:
            for message_ in messages:
                try:
                    bot.send_message(telegram_id, f'you have new message: {message_}')
                except:
                    continue


while True:
    time.sleep(10)
    main_function()
    last_function = datetime.datetime.now() - datetime.timedelta(hours=2)

#bot.infinity_polling()
