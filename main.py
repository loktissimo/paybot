#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
#from subprocess import Popen, PIPE
#import sys,os
import asyncio
import telepot
import telepot.aio
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import urllib.request
import json


#Тут должны находиться ваши айдишники (для примера я сделал 2 разрешенных)
#Вы можете запустить бота и увидеть при нажатии меню или /start ваш личный айдишник
#Ваши разрешенные айди нужно прописать в переменных chat_allow, заменив None на айдишники
chat_allow1=xxxxxxx


#################################
#Блоки дальше - тело самого бота#
#################################

message_with_inline_keyboard = None

#эта функция отвечает за текстовые сообщения и "клавиатуру"
async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type)
    print("id отправителя сообщения: "+str(chat_id))
    if chat_id == chat_allow1 or chat_id == chat_allow2:
        if content_type != 'text':
            return
        else:
            ok=1
        command = msg['text'].lower()
        print(command)

        if command == '/start':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='инфо')],
            [dict(text='управление')],
            [dict(text='скрыть меню')],
            ])
            await bot.sendMessage(chat_id, 'чем воспользуешься?', reply_markup=markup)

        elif command == 'инфо':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='add IP to .onion')],
            [dict(text='управление')],
            [dict(text='скрыть меню')],
            ])
            await bot.sendMessage(chat_id, 'выбери раздел', reply_markup=markup)

        elif command[0] == '!':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='инфо')]
            ])
            command = command.strip('!')
            pcommand = command.replace('.' , '')
            #await bot.sendMessage(chat_id, '%s' %command, reply_markup=markup)
            if pcommand.isalpha():
                address = 'dig +short ' + command
                h = subprocess.getoutput(address)
                subprocess.run(['ipset',  '-A', 'blocklist', h])
                await bot.sendMessage(chat_id, '%s добавлен в ipset' %h, reply_markup=markup)
            elif pcommand.isdigit():
                h = command
                subprocess.run(['ipset',  '-A', 'blocklist', h])
                await bot.sendMessage(chat_id, '%s добавлен в ipset' %h, reply_markup=markup)

        elif command[0] == '#':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='инфо')]
            ])
            h = subprocess.getoutput(command.strip('#'))
            await bot.sendMessage(chat_id, '%s' %h, reply_markup=markup)

        elif command[0] == '@':
            markup = ReplyKeyboardRemove()
            number = command.strip('@')
            url = 'http://www.megafon.ru/api/mfn/info?msisdn=' + number
            response = urllib.request.urlopen(url)
            content = response.read().decode(response.headers.get_content_charset())
            j = json.loads(content)
            #print('{0}: {1} - {2}'.format(number, j['operator'], j['region']))
            #await bot.sendMessage(chat_id, '%s: %s - %s' %number %j['operator'] %j['region'], reply_markup=markup)
            await bot.sendMessage(chat_id, '{0}: {1} - {2}'.format(number, j['operator'], j['region']), reply_markup=markup)

        elif command == 'c':
            markup = ReplyKeyboardMarkup(keyboard=[
            ['Plain text', KeyboardButton(text='Text only')],
            [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
            ])
            await bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)

        elif command == 'управление':
            markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Press me', callback_data='press')],
            ])
            await bot.sendMessage(chat_id, 'Inline keyboard', reply_markup=markup)

        elif command == 'скрыть меню':
            markup = ReplyKeyboardRemove()
            await bot.sendMessage(chat_id, 'Commands starts with # or !', reply_markup=markup)

        else:
            #если ввели текст, не соответствующий команде
            await bot.sendMessage(chat_id, str("начните чат с команды /start"))

    else:
        #если чат айди не соответствует разрешенному
        markup_protect = ReplyKeyboardMarkup(keyboard=[[dict(text='еще раз можно?')]])
        await bot.sendMessage(chat_id, 'Вы не имеете доступа к этому боту!', reply_markup=markup_protect)
        return


#эта функция отвечает за "волшебные полупрозрачные кнопки"
async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, data)
    id_owner_callback=msg['from']['id']
    print("id отправителя запроса: "+str(id_owner_callback))
    if id_owner_callback == chat_allow1 or id_owner_callback == chat_allow2:
        await bot.answerCallbackQuery(query_id, text='Got it', show_alert=False)

        '''
        #управление сигнализацией температуры
        elif data == 'temp_on':
            inf = str(alert_f('on', temper_id))
            await bot.answerCallbackQuery(query_id, text='%s' %inf, show_alert=True)
        elif data == 'temp_off':
            inf = str(alert_f('off', temper_id))
            await bot.answerCallbackQuery(query_id, text='%s' %inf, show_alert=True)
        elif data == 'temp_alert_info':
            inf = str(alert_info_f(temper_id))
            info_c_t = str(c_t_read())
            inf = inf+info_c_t
            await bot.answerCallbackQuery(query_id, text='%s' %inf, show_alert=True)
        elif data == 'temp_alert_min':
            id_write_critical_temper = 1
            await bot.answerCallbackQuery(query_id, text='Установите min порог срабатывания температурной сигнализации. Введите целое число.', show_alert=True)
        else:
            next=1'''
    else:
        await bot.answerCallbackQuery(query_id, text='У вас нет доступа', show_alert=True)


#В TOKEN должен находиться ваш токен, полученый при создании бота!
#замените значение на свои данные!
TOKEN = ""

bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()

#вызов списка ваших функций для работы с api
loop.create_task(bot.message_loop({'chat': on_chat_message,
                                   'callback_query': on_callback_query}))
#project: home-smart-home.ru
print('Listening ...')
loop.run_forever()
