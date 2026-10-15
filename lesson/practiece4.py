from email.mime import text

import telebot
import requests
import json

bot = telebot.TeleBot ('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
API = 'bd85dc84df94cd77fc3178ff6d3dc29b'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт, радий тебе бачити! Напиши назву міста')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        hum = data["main"]["humidity"]
        desc = data["weather"][0]["description"]

        if temp < 10:
            advice = "Вдягайся тепліше!"
        elif 10 <= temp <= 25:
            advice = "Погода чудова для прогулянки!"
        else:
            advice = "На вулиці спека, візьми воду!"

        text_reply = f"Погода у {city}:\nТемпература: {temp}°C\nВідчуття: {feels}°C\nВологість: {hum}%\nОпис: {desc}\nПорада: {advice}"

        bot.reply_to(message, text_reply)

    else:  # ✅ один рівень з if res.status_code
        bot.reply_to(message, "Ви ввели щось не те!")

#     if res.status_code == 200:
#         data = json.loads(res.text)
#
#         temp = data ["main"]["temp"]
#         feels = data ["main"]["feels_like"]
#         hum = data ["main"]["humidity"]
#         desc = data ["weather"][0]["description"]
#
#     if temp < 10:
#         advice = "Вдягайся тепліше!"
#     elif 10 <= temp <= 25:
#         advice = "Погода чудова для прогулянки!"
#     else:
#         advice = "На вулиці спека візьми воду!"
#
#     text_reply = f'Погода у {city}:\nТемпература: {temp}C\nВідчуття: {feels}\nВологість: {hum}%\nОпис: {desc}\n\nПорада: {advice}'
#     bot.reply_to(message, text_reply)
#     else:
# bot.reply_to(message, f"Ви ввели щось не те!")




bot.polling(non_stop=True)