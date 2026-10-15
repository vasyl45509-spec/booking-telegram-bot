from aiogram import Bot, Dispatcher, executor, types
import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_invoice(chat_id=message.chat.id, title='Купівля курса', description='Купівля курса від Програміста', provider_token=config.PAYMENT_TOKEN, currency='UAH',
                           prices=[types.LabeledPrice(label='Купівля курса', amount=10000)], start_parameter='course-payment', payload='invoice-payload-123')


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    await message.answer(f'Success: {message.successful_payment.order_info}')


@dp.pre_checkout_query_handler(lambda query:True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

        

executor.start_polling(dp)