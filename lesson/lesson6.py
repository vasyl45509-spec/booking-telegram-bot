
from aiogram import Bot, Dispatcher, executor, types


bot = Bot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
dp = Dispatcher(bot)


@dp.message_handler(content_types=['photo'])  #commands=['start']
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, 'hello')
    # await message.answer('hello')
    await message.reply('hello')
    # file = open('/some.jpd', 'rb')
    # await message.answer_photo(file)


@dp.message_handler(commands=['inline'])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Site', url='https://google.com'))
    markup.add(types.InlineKeyboardButton('hello', callback_data='hello'))
    await message.reply('Hello', reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


@dp.message_handler(commands=['reply'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Sait'))
    markup.add(types.KeyboardButton('Website'))
    await message.answer('Hello', reply_markup=markup)



executor.start_polling(dp)



