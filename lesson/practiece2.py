import telebot
from telebot import types

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("Наш сайт", url= 'https://google.com')
    btn2 = telebot.types.InlineKeyboardButton("Скажи привіт", callback_data='sey Hello')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Обери дію:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(callback):
    if callback.data == 'say hallo':
        bot.send_message(callback.message.chat.id, 'Привіт від бота')



bot.polling(non_stop=True)