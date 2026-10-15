# import telebot
# import sqlite3
#
# bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
# name =None
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     conn = sqlite3.connect('itproger.sqrl')
#     cur = conn.cursor()
#
#     cur.execute('CREATE TABLE IF NOT EXISTS user (id int auto_increment primary key, name varchar(50), pass varchar(50))')
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     bot.send_message(message.chat.id, 'Привіт зараз тебе зареєструємо! Введіт ваше імя')
#     bot.register_next_step_handler(message, user_name)
#
# def user_name(message):
#     global name
#     name = message.text.strip()
#     bot.send_message(message.chat.id, 'Введіт пароль')
#     bot.register_next_step_handler(message, user_pass)
#
# def user_pass(message):
#     password = message.text.strip()
#
#     conn = sqlite3.connect('itproger.sqrl')
#     cur = conn.cursor()
#
#     cur.execute("INSERT INTO user(name, pass) VALUES ('%s', '%s') " %(name, password))
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton('Список користувача', callback_data='users'))
#     bot.send_message(message.chat.id, 'Користувач зареєстрований!', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('itproger.sqrl')
#     cur = conn.cursor()
#
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
#
#     info = ''
#     for el in users:
#         info += f'Імя: {el[1]}, пароль: {el[2]}\n'
#
#     cur.close()
#     conn.close()
#
#     bot.send_message(call.message.chat.id, info)
#
# bot.polling(none_stop=True)


import sqlite3
import telebot

bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

name = ''


@bot.message_handler(commands=['start'])
def start(message):
  conn = sqlite3.connect('itproger.sql')
  cur = conn.cursor()

  # Створення таблиці (виправлено синтаксис SQLite)
  cur.execute(
      'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,'
      ' name text, pass text)'
  )
  conn.commit()
  cur.close()
  conn.close()

  bot.send_message(
      message.chat.id, "Привіт, зараз тебе зареєструємо! Введіть ваше ім'я"
  )
  bot.register_next_step_handler(message, user_name)


def user_name(message):
  global name
  name = message.text.strip()
  bot.send_message(message.chat.id, 'Введіть пароль')
  bot.register_next_step_handler(message, user_pass)


def user_pass(message):
  password = message.text.strip()

  conn = sqlite3.connect('itproger.sql')
  cur = conn.cursor()
  cur.execute(
      'INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password)
  )
  conn.commit()
  cur.close()
  conn.close()

  markup = telebot.types.InlineKeyboardMarkup()
  markup.add(
      telebot.types.InlineKeyboardButton(
          'Список користувачів', callback_data='users'
      )
  )
  bot.send_message(
      message.chat.id, 'Користувача зареєстровано!', reply_markup=markup
  )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
  conn = sqlite3.connect('itproger.sql')
  cur = conn.cursor()

  cur.execute('SELECT * FROM users')
  users = cur.fetchall()

  info = ''
  for el in users:
    info += f"Ім'я: {el[1]}, пароль: {el[2]}\n"

  cur.close()
  conn.close()

  bot.send_message(call.message.chat.id, info)


bot.polling(non_stop=True)
