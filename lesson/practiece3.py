import telebot
import sqlite3


bot = telebot.TeleBot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('notes.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text text)')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привіт! Напиши мені нотатку...')
    bot.register_next_step_handler(message, save_note)

def save_note(message):
    note_text = message.text.strip()
    conn = sqlite3.connect('notes.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (text) VALUES ("%s")' % note_text)
    conn.commit()
    cur.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Показати всі нотатки', callback_data='show_notes'))

    bot.send_message(message.chat.id, 'Нотатку збережено!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    conn = sqlite3.connect('notes.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM NOTES')
    notes = cur.fetchall()

    info = ''
    for note in notes:
        info += f"*{note[1]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(non_stop=True)