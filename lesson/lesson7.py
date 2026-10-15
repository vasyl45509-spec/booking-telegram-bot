from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_data import WebAppData

bot = Bot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_btn = types.KeyboardButton('Відкрити веб сторінку', web_app=types.WebAppInfo(url='https://meek-kitsune-d0ca6e.netlify.app'))
    markup.add(web_app_btn)
    await message.answer('Привіт мій друже', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def web_data(message: types.Message):
    await message.answer(f"Отримано з сайту: {message.web_app_data.data}")

executor.start_polling(dp)