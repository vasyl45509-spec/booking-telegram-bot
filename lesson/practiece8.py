from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton

from lesson import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(InlineKeyboardButton(text='Course',callback_data='buy_course'))
    markup.add(InlineKeyboardButton(text='VIP',callback_data='buy_vip'))

    await message.reply('Привіт', reply_markup=markup)

@dp.callback_query_handler(text=['buy_course', 'buy_vip'])
async def call(callback):
    if callback.data == 'buy_course':
        # await callback.message.answer("Ви обрали курс!")
        await bot.send_invoice(chat_id=callback.message.chat.id, title='Курс', description='Крутий курс від програміста', payload='peyload_course',
                               provider_token=config.PAYMENT_TOKEN, currency='EUR', prices=[types.LabeledPrice(label='Курс', amount=10000)])
    elif callback.data == 'buy_vip':
        # await callback.message.answer("Ви обрали курс!")
        await bot.send_invoice(chat_id=callback.message.chat.id, title='VIP-чат', description='Доступ до закритого чату!',
                               payload='peyload_vip', provider_token=config.PAYMENT_TOKEN, currency='UAH',
                               prices=[types.LabeledPrice(label='Курс', amount=5000)])

    await callback.answer()


@dp.pre_checkout_query_handler(lambda query:True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    payload = message.successful_payment.invoice_payload
    if payload == 'payload_course':
        await message.answer("Дякуємо за покупку! Ось посилання на курс: [посилання]")
    elif payload == 'payload_vip ':
        await message.answer("Ласкаво просимо до VIP! Посилання: ...")




executor.start_polling(dp)