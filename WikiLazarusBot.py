import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

bot = telebot.TeleBot("", parse_mode=None)
bot.remove_webhook()
#'https://wiki.lazarus.freepascal.org/index.php?title=Special%3ASearch&search={0}&fulltext=Search'.format(message.text)
@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите запрос поиска')
    bot.register_next_step_handler(msg, create_request)


def create_request(message):
    #bot.send_message(message.chat.id, message.text)
    result_list = []
    r = requests.get('https://wiki.lazarus.freepascal.org/index.php?title=Special%3ASearch&search={0}&fulltext=Search'.format(message.text))
    soup = bs(r.text, "html.parser")
    List_names = soup.find_all('li', class_='mw-search-result')
    for info in List_names:
        result_list.append(info.a['title']+': https://wiki.lazarus.freepascal.org'+info.a['href'])
    bot.send_message(message.chat.id, '\n'.join(result_list))
    
if __name__ == '__main__':
    bot.infinity_polling()