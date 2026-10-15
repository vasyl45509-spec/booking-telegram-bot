# app/keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests as rq

# Головне меню, яке з'явиться після реєстрації
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📝 Записатися')],
    [KeyboardButton(text='🗓 Мої записи'), KeyboardButton(text='ℹ️ Про нас')]
], resize_keyboard=True)

# Клавіатура для запиту номера телефону
request_phone = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📱 Відправити свій номер', request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)


# app/keyboards.py
# Головне меню
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📝 Записатися')],
    [KeyboardButton(text='🗓 Мої записи')],
    [KeyboardButton(text='👦 Наші майстри')],
    [KeyboardButton(text='❕ Про нас')]
], resize_keyboard=True)

# Запит телефону
request_phone = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📱 Відправити свій номер', request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)


# Головне меню адміна
admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📋 Усі записи клієнтів", callback_data="admin_all_bookings")],
        [InlineKeyboardButton(text="➕ Додати послугу", callback_data="admin_add_service")],
        [InlineKeyboardButton(text="➕ Додати майстра", callback_data="admin_add_master")]
    ]
)

# Генерація кнопок із послугами з БД
async def services_keyboard():
    keyboard = InlineKeyboardBuilder()
    services = await rq.get_services()
    for service in services:
        keyboard.add(InlineKeyboardButton(text=f"{service.name} — {service.price} грн", callback_data=f"service_{service.id}"))
    return keyboard.adjust(1).as_markup()

# Генерація кнопок із майстрами з БД
async def masters_keyboard():
    keyboard = InlineKeyboardBuilder()
    masters = await rq.get_masters()
    for master in masters:
        keyboard.add(InlineKeyboardButton(text=master.name, callback_data=f"master_{master.id}"))
    return keyboard.adjust(1).as_markup()


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cancel_booking_kb(booking_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Скасувати запис", callback_data=f"cancel_{booking_id}")]
    ])


