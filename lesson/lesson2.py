import telebot
from telebot import types

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт 😀')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалити фото')
    btn3 = types.KeyboardButton('Поміняти текс')
    markup.row(btn2, btn3)
    file = open('./7dd54f6bf3060c4f510220a5fb82aa6cef9c5a6a-1694447704.jpg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup = markup)
    # bot.send_audio(message.chat.id, file, reply_markup=markup)
    # bot.send_video(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, 'Привіт', reply_markup = markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалити фото':
        bot.send_message(message.chat.id, 'delete')




@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = (types.InlineKeyboardButton('Перейти на сайт', url='https://itproger.com'))
    markup.row(btn1)
    btn2 = (types.InlineKeyboardButton('Удалити фото', callback_data='delete'))
    btn3 = (types.InlineKeyboardButton('Поміняти текс', callback_data='edit'))
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Вау гарне фото!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
       bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)




bot.polling(none_stop=True)