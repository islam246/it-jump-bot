import traceback

from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext import Updater
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functools import wraps

import time
import telegram
import pickle
import os


token = '923822935:AAE8wF5-lww9K2SOigwD370-bYvrJ1_XUHk'
bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
chats_file = 'chats.txt'
chats = pickle.load(open(chats_file, 'rb')) if os.path.exists(chats_file) else {}
print(bot.get_me())


def catch_error(f):
    @wraps(f)
    def wrap(update, context):
        try:
            return f(update, context)
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, text="Error occured: " )
            print(traceback.format_exc())

    return wrap


@catch_error
def start(update, context):
    print('received', update.message.chat_id)
    chats.add(update.message.chat_id)
    with open(chats_file, 'wb') as file:
        pickle.dump(chats, file)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Я бот Peter.")


@catch_error
def distance_google(location_from, location_where):
    l_from = location_from #1)как работать с городами у которых раздельное название?
    l_where = location_where #2)как работать с городами которые настолько далеко, что мапа показывает только авиабилет?
    driver = webdriver.Chrome()
    driver.get('https://www.google.ru/maps/')

    itinerary = driver.find_element_by_xpath('//*[@id="searchbox-directions"]')
    itinerary.click()  # допилить чтоб драйвер не ждал загрузку всей страницы
    time.sleep(8)


    departure_input = driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input')
    departure_input.send_keys(l_from)


    destination_input = driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input')
    destination_input.send_keys(l_where)
    destination_input.send_keys(Keys.ENTER)
    time.sleep(3)
    t = driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div[2]/div[1]/div[1]/div[2]/div')
    return t.text


@catch_error
def text(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Привет!")
    elif text.lower().startswith('расстояние '): #check distance_google
        _, l_from, l_where = text.split(' ')
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Расстояние между {l_from} и {l_where} {distance_google(l_from,l_where)}")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Такой команды не существует.\n"
                                                                       "Есть: \n"
                                                                       '1.расстояние [откуда] [куда]')



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(text_handler)

updater.start_polling()