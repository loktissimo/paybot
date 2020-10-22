# -*- coding: utf-8 -*-
import telebot  # TelegramBot API
from telebot import types  # inline Keyboards
import logging  # internet errors
import time  # internet errors
from datetime import datetime  # unix timestamp parsing
import config  # import config.py (Token setting, etc)
import paybotdbworker  # import SQLite custom functions
import json
from pprint import pprint

bot = telebot.TeleBot(config.token)


bot.remove_webhook()  # Removing webhook from Flask server (Flask is a side project)
time.sleep(1)


# Обработчик команды '/hello'.
@bot.message_handler(commands=['hello'])
def handle_hello_command(message):
    if message.chat.type == 'group':
        # '/hello' запускается только из группового чата
        hello_msg = ('Привет! Я Бот для расчётов. \n\n'
                     'Для участия в расчётах - жми кнопку \U0001F44D\n\n'
                     '*Я знаю такие команды:*\n'
                     '/pay 150 Леденцы\n'
                     '/pay 300 Газировка @Вася @Петя\n'
                     '/eat 25%\n')

        keyboard = types.InlineKeyboardMarkup()
        callback_button_join = types.InlineKeyboardButton(text=u'\U0001F44D Участвовать', callback_data="join")
        keyboard.add(callback_button_join)
        bot.send_message(message.chat.id, hello_msg, parse_mode='Markdown', reply_markup=keyboard)

        if message:
            print('[New chat] ChatID: {}; Title: {}'.format(message.chat.id, message.chat.title))
            paybotdbworker.new_chat(message.chat.id, message.chat.title)

    else:
        # В приватном и други чатах отвечает только "Привет"
        print('[Private chat] UserName: {}'.format(message.from_user.first_name))
        bot.send_message(message.chat.id, 'Привет!')


# Обработчик команды '/pay'.
@bot.message_handler(commands=['pay'])
def handle_pay_command(message):
    pay_list = message.text.split()[1:]

    # print('m.text: ' + message.text, pay_list, len(pay_list))
    # print(message)
    # unix time to human format
    # timestamp = datetime.fromtimestamp(message.date)
    # print(timestamp.strftime('%d-%m-%Y'))  # print human format date

    if not pay_list or len(pay_list) < 2 or not pay_list[0].isdigit():
        print('[Pay] Syntax error')
        bot.reply_to(message, 'Пиши так: /pay 100 леденцы', parse_mode='Markdown')
    else:
        print('[Pay] ChatID: {}, Title: {}, UserID: {}: Text: {}'.format(
            message.chat.id, message.from_user.first_name, message.from_user.id, message.text)
        )
        paybotdbworker.new_post(message.date, message.text, message.chat.id, message.from_user.id)
        bot.reply_to(message, 'Записал')


# Обработчик команды '/eat'.
@bot.message_handler(commands=['eat'])
def handle_pay_command(message):
    print('[Eat] command')


# Обработчик _изменений_ к командам '/pay' и '/eat'.
@bot.edited_message_handler(commands=['pay', 'eat'])
def handle_edit_command(message):
    print('[Pay] edited message: {}'.format(message.text))
    paybotdbworker.update_post(message.date, message.text)
    edited_list = message.text.split()[1:]
    # print(edited_list, len(edited_list))
    bot.send_message(message.chat.id, 'Изменения: {}'.format(edited_list, len(edited_list)))


# Обработчик команды '/stat'.
@bot.message_handler(commands=['stat'])
def handle_pay_command(message):
    timestamp = datetime.fromtimestamp(message.date)  # unix time to human format
    print('[Stat] for UserName: {} shown at {}'.format(
        message.from_user.first_name, timestamp.strftime('%H:%M %d-%m-%Y'))
    )
    bot.send_message(message.chat.id, '```Статистика:```', parse_mode='Markdown')


# Test function
@bot.message_handler(content_types=['contact'])
def handle_text_doc(message):
    print('Got Contact!')


#
@bot.message_handler(commands=['leave'])
def handle_leave_command(message):
    #   markup = types.ReplyKeyboardMarkup()
    #   markup.row('Start', 'Help', 'Pay')
    #   bot.send_message(message.chat.id, 'Описание работы бота: /n/n Строка 1', reply_markup=markup)
    bot.send_message(message.chat.id, 'Описание работы бота: \n \nСтрока 1\nСтрока 2\nКомманда /join')


# Обычный режим
@bot.message_handler(content_types=['text'])
def any_msg(message):

    print(message)

    if message.entities:
        print('{} entities in message'.format(len(message.entities)))
        for entity in message.entities:
            entity_text = message.text[entity.offset:entity.offset + entity.length]
            print('entity text: ' + format(entity_text))

    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='Нажми меня', callback_data='test')
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Сообщение в ответ', reply_markup=None)  # reply_markup=keyboard


# Обработчик нажатий кнопок на экране
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "join":
            print('[New user] UserID: {}, First name: {}'.format(call.from_user.id, call.from_user.first_name))
            paybotdbworker.new_user(call.from_user.id, call.from_user.username , call.from_user.first_name)
            bot.send_message(call.message.chat.id,
                             text='Ура! {} присоединилися к расчётам.'.format(call.from_user.first_name))


# Запуск poller'a
if __name__ == '__main__':
    print('PayBot is listening...')
    # bot.polling(none_stop=True)
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            logging.error(err)
            time.sleep(10)
            print('Internet error!')
