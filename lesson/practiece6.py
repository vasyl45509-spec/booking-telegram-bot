from aiogram import Bot, Dispatcher, executor, types
import random

bot = Bot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
dp = Dispatcher(bot)


facts = [  "Перша комп'ютерна гра з'явилася у 1958 році — це був тенісний симулятор.",
    "Python назвали на честь комедійного шоу 'Літаючий цирк Монті Пайтона', а не змії.",
    "Перший у світі вебсайт все ще працює в інтернеті з 1991 року.",
    "Мова JavaScript була створена всього за 10 днів."]




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('🎲 Отримати факт')
    markup.add(btn)
    await message.answer("Привіт! Натисни кнопку нижче, щоб дізнатися новий факт!", reply_markup=markup)


@dp.message_handler(text=['🎲 Отримати факт'])
async def send_fact(message: types.Message):
    random_fact = random.choice(facts)

    inline_markup = types.InlineKeyboardMarkup()
    btn1 =types.InlineKeyboardButton("Ще один 🔄", callback_data="more_facts")
    inline_markup.add(btn1)
    await message.answer(random_fact, reply_markup=inline_markup)


@dp.callback_query_handler(text="more_facts")
async def process_more_facts(call: types.CallbackQuery):
    random_fact = random.choice(facts)

    inline_markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Ще один 🔄", callback_data="more_facts")
    inline_markup.add(btn1)

    await call.answer()

    await call.message.answer(random_fact, reply_markup=inline_markup)




executor.start_polling(dp)