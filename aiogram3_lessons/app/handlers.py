from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин кроссовок!', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$')


# handlers.py

# 1. Показ картки товару з кнопкою "Додати в кошик"
# handlers.py
@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item_data = await rq.get_item(item_id)
    await callback.answer()
    await callback.message.answer(
        f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$',
        reply_markup=await kb.item_card(item_data.id, item_data.category)  # <-- Змінити на item_card!
    )



# 2. Обробка натискання кнопки "Додати в кошик"
@router.callback_query(F.data.startswith('to_basket_'))
async def add_to_basket(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[2])
    await rq.set_basket(callback.from_user.id, item_id)
    await callback.answer('Товар додано в кошик!', show_alert=True)


# 3. Перегляд кошика за кнопкою з головного меню
@router.message(F.text == 'Корзина')
async def show_basket(message: Message):
    basket_items = await rq.get_basket(message.from_user.id)

    if not basket_items:
        await message.answer('Ваш кошик порожній.')
        return

    text = "🛒 **Ваш кошик:**\n\n"
    total_price = 0

    for item in basket_items:
        text += f"• {item.name} — {item.price}$\n"
        total_price += item.price

    text += f"\n**Разом до сплати:** {total_price}$"
    await message.answer(text)
# from email import message
#
# from aiogram import F, Router
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message, CallbackQuery
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext
#
# import app.keyboards as kb
# import app.database.requests as rq
# from app.Middleware import TestMiddleware
#
# router = Router()
# router.message.outer_middleware(TestMiddleware())
#
# # class Reg(StatesGroup):
# #     name = State()
# #     number = State()
#
# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await rq.set_user(message.from_user.id)
#     await message.answer('Вітаємо в магазині кросівок!', reply_markup=kb.main)
#
# @router.message(F.text == 'Каталог')
# async def catalog(message: Message):
#     await message.answer('Виберіть категорію товара!', reply_markup=await kb.categories())
#
#
#
#
# @router.callback_query(F.data.startswith('category_'))
# async def category(callback: CallbackQuery):
#     await callback.answer('Ви вибрали категорію')
#     await callback.message.answer('Виберіть товар по категорії', reply_markup=await kb.items(callback.data.split('_')[1]))
#
# @router.callback_query(F.data.startswith('item_'))
# async def item(callback: CallbackQuery):
#     item_data = await rq.get_item(callback.data.split('_')[1])
#     await callback.answer('Ви вибрали товар')
#     await callback.message.answer(f'Назва: {item_data.name}\nОпис:{item_data.description}\nЦіна:{item_data.price}',
#                                   reply_markup= await kb.items(callback.data.split('_')[1]))



# @router.message(Command('help'))
# async def get_help(message: Message):
#     await message.answer('Це команда /help')
#
# @router.message(F.text == 'Як справи?')
# async def how_are_you(message: Message):
#     await message.answer('OK!')
#
# @router.message(F.photo)
# async def photo(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')
#
# @router.message(Command('get_photo'))
# async def get_photo(message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAIEVWqWwDr2YOk44T_Zj5SLfpCgw9y6AAKsIGsb5ZK4SIXvG3f6YJSBAQADAgADeQADPQQ', #Силку ще можна
#                                caption='Це фото природи!')
#
# @router.callback_query(F.data == 'catalog')
# async def catalog(callback: CallbackQuery):
#     await callback.answer('Ви вибрали каталог', show_alert=True)
#     await callback.message.edit_text('Привіт!', reply_markup=await kb.inline_cars())
#
# @router.callback_query(F.data == 'basket')
# async def basket(callback: CallbackQuery):
#     await callback.answer('Ваш кошик порожній!')
#     await callback.message.edit_text('Ваш кошик порожній оберіть товар:!', reply_markup=await kb.inline_cars())
#
# @router.message(Command('reg'))
# async def first_reg(message: Message, state: FSMContext):
#     await state.set_state(Reg.name)
#     await message.answer('Введіть ваше імя')
#
# @router.message(Reg.name)
# async def second_reg(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Reg.number)
#     await message.answer('Введіть ваш номер')
#
# @router.message(Reg.number)
# async def second_first(message: Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     data = await state.get_data()
#     await message.answer(f'Дякуємо, реєстрація завершена.\nІмя: {data["name"]}\nНомер: {data["number"]}')
#     await state.clear()



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