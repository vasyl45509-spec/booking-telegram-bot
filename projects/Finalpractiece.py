# import sqlite3
# import logging
# from datetime import datetime, timedelta
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# # Налаштування логування, щоб бачити помилки в консолі
# logging.basicConfig(level=logging.INFO)
#
# # Ініціалізація бота (токен залишається твоїм)
# bot = Bot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
# dp = Dispatcher(bot)
#
# DB_NAME = "users.db"
#
# # ==========================================
# #          БЛОК РОБОТИ З БАЗОЮ ДАНИХ (БД)
# # ==========================================
#
# def init_db():
#     """Створює таблицю користувачів із полями балансу та часу останнього бонусу"""
#     with sqlite3.connect(DB_NAME) as conn:
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id INTEGER PRIMARY KEY,
#                 username TEXT,
#                 balance REAL DEFAULT 0.0,
#                 last_bonus TEXT DEFAULT NULL
#             )
#         ''')
#         conn.commit()
#
# def add_user(user_id: int, username: str) -> bool:
#     """Додає юзера в базу. Повертає True, якщо новий, і False, якщо вже є"""
#     try:
#         with sqlite3.connect(DB_NAME) as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 "INSERT INTO users (user_id, username, balance) VALUES (?, ?, 0.0)",
#                 (user_id, username)
#             )
#             conn.commit()
#             return True
#     except sqlite3.IntegrityError:
#         return False
#
# def get_user(user_id: int):
#     """Повертає кортеж: (user_id, username, balance, last_bonus) або None"""
#     with sqlite3.connect(DB_NAME) as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT user_id, username, balance, last_bonus FROM users WHERE user_id = ?", (user_id,))
#         return cursor.fetchone()
#
# def update_bonus_time(user_id: int, amount: float):
#     """Нараховує монети за бонус та записує поточний час у базу"""
#     now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with sqlite3.connect(DB_NAME) as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE users SET balance = balance + ?, last_bonus = ? WHERE user_id = ?",
#             (amount, now_str, user_id)
#         )
#         conn.commit()
#
# def remove_balance(user_id: int, amount: float):
#     """Списує монети з балансу користувача"""
#     with sqlite3.connect(DB_NAME) as conn:
#         cursor = conn.cursor()
#         cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
#         conn.commit()
#
#
# # ==========================================
# #          БЛОК КЛАВІАТУРИ ТА ХЕНДЛЕРІВ
# # ==========================================
#
# # Створюємо головну клавіатуру під чатом
# profile_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# profile_kb.add(KeyboardButton('👤 Мій профіль'), KeyboardButton('💰 Баланс'))
# profile_kb.add(KeyboardButton('🎁 Отримати бонус'), KeyboardButton('🛒 Магазин'))
#
#
# async def on_startup(_):
#     init_db()
#     print("Базу даних підключено успішно!")
#
#
# @dp.message_handler(commands=['start'])
# async def start_cmd(message: types.Message):
#     is_new = add_user(message.from_user.id, message.from_user.username)
#
#     if is_new:
#         await message.answer(f"Вітаю, {message.from_user.first_name}! Я додав тебе в базу даних.",
#                              reply_markup=profile_kb)
#     else:
#         await message.answer(f"З поверненням, {message.from_user.first_name}! Ти вже є в базі.",
#                              reply_markup=profile_kb)
#
#
# @dp.message_handler(text=['👤 Мій профіль'])
# async def show_profile(message: types.Message):
#     user_id = message.from_user.id
#     user_data = get_user(user_id)
#
#     if user_data:
#         # Безпечно дістаємо ID та юзернейм (елементи 0 та 1 з кортежу БД)
#         db_id = user_data[0]
#         username = user_data[1]
#
#         text = (
#             f"<b>👤 Твій профіль:</b>\n\n"
#             f"🆔 <b>ID:</b> <code>{db_id}</code>\n"
#             f"💬 <b>Юзернейм:</b> @{username if username else 'не вказано'}"
#         )
#         await message.answer(text, parse_mode="HTML")
#     else:
#         await message.answer("Тебе чомусь немає в базі. Напиши /start")
#
#
# @dp.message_handler(text=['💰 Баланс'])
# async def show_balance(message: types.Message):
#     user_id = message.from_user.id
#     user_data = get_user(user_id)
#
#     if user_data:
#         balance = user_data[2]  # Третій елемент у базі — це баланс
#         text = (
#             f"💰 <b>Твій баланс:</b> {balance} монет\n"
#             f"📊 <b>Статус:</b> Активний"
#         )
#         await message.answer(text, parse_mode="HTML")
#     else:
#         await message.answer("Тебе немає в базі. Напиши /start")
#
#
# @dp.message_handler(text=['🎁 Отримати бонус'])
# async def get_bonus(message: types.Message):
#     user_id = message.from_user.id
#     user_data = get_user(user_id)
#
#     if not user_data:
#         await message.answer("Тебе немає в базі. Напиши /start")
#         return
#
#     # Четвертий елемент у базі (індекс 3) — це час останнього бонусу
#     last_bonus_str = user_data[3]
#
#     if last_bonus_str:
#         last_bonus_time = datetime.strptime(last_bonus_str, "%Y-%m-%d %H:%M:%S")
#         next_bonus_time = last_bonus_time + timedelta(hours=24)  # Обмеження на 24 години
#
#         if datetime.now() < next_bonus_time:
#             time_left = next_bonus_time - datetime.now()
#             hours = time_left.seconds // 3600
#             minutes = (time_left.seconds % 3600) // 60
#
#             await message.answer(
#                 f"❌ <b>Ви вже отримували бонус!</b>\n"
#                 f"Повертайтеся через <b>{hours} год. {minutes} хв.</b>",
#                 parse_mode="HTML"
#             )
#             return
#
#     # Якщо перевірку часу пройдено, видаємо бонус
#     update_bonus_time(user_id, 10.0)
#     await message.answer("🎉 Вітаю! Ти отримав <b>+10 монет</b> на свій баланс!", parse_mode="HTML")
#
#
# @dp.message_handler(text=['🛒 Магазин'])
# async def show_shop(message: types.Message):
#     text = (
#         "🛒 <b>Ласкаво просимо до магазину!</b>\n\n"
#         "⭐ <b>VIP-статус</b> — 50 монет\n"
#         "<i>Щоб купити VIP, напиши команду:</i> /buy_vip"
#     )
#     await message.answer(text, parse_mode="HTML")
#
#
# @dp.message_handler(commands=['buy_vip'])
# async def buy_vip(message: types.Message):
#     user_id = message.from_user.id
#     user_data = get_user(user_id)
#
#     if user_data:
#         balance = user_data[2]  # Отримуємо поточний баланс з бази
#
#         if balance >= 50.0:
#             remove_balance(user_id, 50.0)  # Списуємо 50 монет
#             await message.answer("🎉 <b>Вітаю!</b> Ти успішно придбав VIP-статус!", parse_mode="HTML")
#         else:
#             need_more = 50.0 - balance
#             await message.answer(f"❌ <b>Недостатньо монет!</b> Тобі бракує ще {need_more} монет.", parse_mode="HTML")
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


import sqlite3
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# 📥 Імпортуємо Inline-кнопки для красивого посилання
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

bot = Bot('8604300204:AAE5wipm9RMbOM3OYFq40R9SpKn6ftSvv_w')
dp = Dispatcher(bot)

DB_NAME = "users.db"

# ==========================================
#          БЛОК РОБОТИ З БАЗОЮ ДАНИХ (БД)
# ==========================================

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance REAL DEFAULT 0.0,
                last_bonus TEXT DEFAULT NULL
            )
        ''')
        conn.commit()

def add_user(user_id: int, username: str) -> bool:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, username, balance) VALUES (?, ?, 0.0)",
                (user_id, username)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def get_user(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, balance, last_bonus FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def update_bonus_time(user_id: int, amount: float):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET balance = balance + ?, last_bonus = ? WHERE user_id = ?",
            (amount, now_str, user_id)
        )
        conn.commit()

def remove_balance(user_id: int, amount: float):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
        conn.commit()


# ==========================================
#          БЛОК КЛАВІАТУРИ ТА ХЕНДЛЕРІВ
# ==========================================

profile_kb = ReplyKeyboardMarkup(resize_keyboard=True)
profile_kb.add(KeyboardButton('👤 Мій профіль'), KeyboardButton('💰 Баланс'))
profile_kb.add(KeyboardButton('🎁 Отримати бонус'), KeyboardButton('🛒 Магазин'))
# ✨ Додаємо нову просту кнопку під чат:
profile_kb.add(KeyboardButton('📞 Контакти'))


# 🔗 Створюємо інлайн-кнопку (посилання), яка з'явиться під повідомленням контакту
contact_inline_kb = InlineKeyboardMarkup()
# Заміни "твій_юзернейм" на свій нік в Телеграмі без знаку @
contact_inline_kb.add(InlineKeyboardButton(text="💬 Написати менеджеру", url="https://t.me"))


async def on_startup(_):
    init_db()
    print("Базу даних підключено успішно!")


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    is_new = add_user(message.from_user.id, message.from_user.username)

    if is_new:
        await message.answer(f"Вітаю, {message.from_user.first_name}! Я додав тебе в базу даних.",
                             reply_markup=profile_kb)
    else:
        await message.answer(f"З поверненням, {message.from_user.first_name}! Ти вже є в базі.",
                             reply_markup=profile_kb)


# 🔥 НОВИЙ ПРОСТИЙ ХЕНДЛЕР: реагує на кнопку "📞 Контакти"
@dp.message_handler(text=['📞 Контакти'])
async def show_contacts(message: types.Message):
    text = (
        "📞 <b>Зв'язок з адміністрацією</b>\n\n"
        "Якщо у вас виникли питання, проблеми з балансом або пропозиції щодо співпраці — натисніть на кнопку нижче, щоб написати нашому менеджеру прямо в приватні повідомлення!"
    )
    # Відправляємо текст разом із інлайн-кнопкою
    await message.answer(text, parse_mode="HTML", reply_markup=contact_inline_kb)


# ==========================================
#          СТАРІ СТАНДАРТНІ КНОПКИ
# ==========================================

@dp.message_handler(text=['👤 Мій профіль'])
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if user_data:
        db_id = user_data
        username = user_data

        text = (
            f"<b>👤 Твій профіль:</b>\n\n"
            f"🆔 <b>ID:</b> <code>{db_id}</code>\n"
            f"💬 <b>Юзернейм:</b> @{username if username else 'не вказано'}"
        )
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("Тебе чомусь немає в базі. Напиши /start")


@dp.message_handler(text=['💰 Баланс'])
async def show_balance(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if user_data:
        balance = user_data
        text = (
            f"💰 <b>Твій баланс:</b> {balance} монет\n"
            f"📊 <b>Статус:</b> Активний"
        )
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("Тебе немає в базі. Напиши /start")


@dp.message_handler(text=['🎁 Отримати бонус'])
async def get_bonus(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if not user_data:
        await message.answer("Тебе немає в базі. Напиши /start")
        return

    last_bonus_str = user_data

    if last_bonus_str:
        last_bonus_time = datetime.strptime(last_bonus_str, "%Y-%m-%d %H:%M:%S")
        next_bonus_time = last_bonus_time + timedelta(hours=24)

        if datetime.now() < next_bonus_time:
            time_left = next_bonus_time - datetime.now()
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60

            await message.answer(
                f"❌ <b>Ви вже отримували бонус!</b>\n"
                f"Повертайтеся через <b>{hours} год. {minutes} хв.</b>",
                parse_mode="HTML"
            )
            return

    update_bonus_time(user_id, 10.0)
    await message.answer("🎉 Вітаю! Ти отримав <b>+10 монет</b> на свій баланс!", parse_mode="HTML")


@dp.message_handler(text=['🛒 Магазин'])
async def show_shop(message: types.Message):
    text = (
        "🛒 <b>Ласкаво просимо до магазину!</b>\n\n"
        "⭐ <b>VIP-статус</b> — 50 монет\n"
        "<i>Щоб купити VIP, напиши команду:</i> /buy_vip"
    )
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=['buy_vip'])
async def buy_vip(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if user_data:
        balance = user_data

        if balance >= 50.0:
            remove_balance(user_id, 50.0)
            await message.answer("🎉 <b>Вітаю!</b> Ти успішно придбав VIP-статус!", parse_mode="HTML")
        else:
            need_more = 50.0 - balance
            await message.answer(f"❌ <b>Недостатньо монет!</b> Тобі бракує ще {need_more} монет.", parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
