
import telebot
import webbrowser

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

@bot.message_handler(commands=['site', 'website'])
def site(messege):
    webbrowser.open('https://itproger.com')


@bot.message_handler(commands=['start', 'main', 'hallo'])
def main(message):
    bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id,'<b>Help</b> <em><u>information</u></em>', parse_mode='html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привіт':
        bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

bot.polling(none_stop=True)
