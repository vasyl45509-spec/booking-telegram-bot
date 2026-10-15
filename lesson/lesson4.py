

import telebot
import requests
import json

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
API = 'bd85dc84df94cd77fc3178ff6d3dc29b'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт, радий тебе бачити! Напиши назву міста')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res =requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Зараз погода: {temp}')



        image = 'depositphotos_12492703-stock-photo-summer-hot-sun.jpg' if temp > 5.0 else 'images.jpg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Місто вказане не правильне!')



bot.polling(none_stop=True)