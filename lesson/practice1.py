
import telebot

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт напиши мені щось!')

@bot.message_handler(commands=['halp'])
def halp(message):
    bot.send_message(message.chat.id, 'Я бот-помічник.Можу повторювати твої слова.')


@bot.message_handler(content_types=['text'])
def info(message):
        bot.send_message(message.chat.id, f'Ти написав: {message.text}')




bot.polling(none_stop= True)