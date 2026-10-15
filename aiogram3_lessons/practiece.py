# import asyncio
# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message
#
# from config import TOKEN
#
# bot = Bot(token=TOKEN)
# dp = Dispatcher()
#
# # --- СУДИ ПИШЕМО ПРАКТИКУ ---
# @dp.message(Command('about'))
# async def about(message: Message):
#     await message.reply("Я бот, створений для навчання Aiogram 3!")
#
# @dp.message(F.text == 'Хто ти?')
# async def why(message: Message):
#     await message.answer("Я твій новий помічник!")
#
# @dp.message(F.photo)
# async def get_photo(message: Message):
#     await message.answer(f"Дякую за фото! Його ID: {message.photo[-1].file_id}")
#
#
# # У keyboards.py
# items = ['Каталог', 'Кошик', 'Контакти']
#
#
#
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print('Exit')


# from aiogram import F, Router
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message, CallbackQuery
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext
#
#
#
#
# router = Router()
#
#
# class Order(StatesGroup):
#     item = State()
#     age = State()
#
# @router.message(Command('order'))
# async def first_order(message: Message, state: FSMContext):
#     await state.set_state(Order.item)
#     await message.answer('Що бажаєте замовити?')
#
# @router.message(Order.item)
# async def second_order(message: Message, state: FSMContext):
#     await state.update_data(item=message.text)
#     await state.set_state(Order.age)
#     await message.answer('Вкажіть ваш вік')
#
# @router.message(Order.age)
# async def second_firs(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer('Будь ласка введіть вік числом!')
#         return
#     await state.update_data(age=message.text)
#     data = await state.get_data()
#     await message.answer(f'Замовлення прийнято!\nТовар: {data["item"]}\nВік: {data["age"]}')
#     await state.clear()






