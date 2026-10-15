from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from datetime import datetime
from config1 import ADMIN_ID


import app.keyboards as kb
import app.states as st
import app.database.requests as rq
from app.database.models import Master, Booking
from app.keyboards import cancel_booking_kb
from app.database.requests import get_all_bookings, get_services

router = Router()

# 1. Точка входу: /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "Вітаю! Ви потрапили в бот для бронювання послуг.\nБудь ласка, введіть ваше ім'я:"
    )
    await state.set_state(st.Reg.name)


# Спрацює як на команду /cancel, так і на кнопку/текст "Скасувати"
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "скасувати")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    # Якщо користувач не перебуває в жодному стані — нічого скасовувати
    if current_state is None:
        await message.answer("Немає активних дій для скасування.")
        return

    # Очищаємо стан та всі збережені тимчасові дані
    await state.clear()
    await message.answer(
        "❌ Дійю скасовано. Ви повернулися в головне меню.",
        reply_markup=ReplyKeyboardRemove()  # Прибираємо спеціальні клавіатури (наприклад, кнопку телефону)
    )


# 2. Ловимо ім'я
@router.message(st.Reg.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()

    # Валідація: перевіряємо довжину та наявність лише літер
    is_valid_len = 2 <= len(name) <= 25
    is_valid_chars = name.replace("-", "").replace(" ", "").isalpha()

    # Якщо ім'я НЕ пройшло перевірку
    if not is_valid_len or not is_valid_chars:
        # 1. Беремо поточні дані зі стану
        data = await state.get_data()
        attempts = data.get("name_attempts", 0) + 1  # Додаємо +1 спробу

        # 2. Якщо це вже 3-тя спроба — скидаємо стан
        if attempts >= 3:
            await state.clear()
            await message.answer(
                "❌ Забагато некоректних спроб. Реєстрацію скасовано.\n"
                "Спробуйте розпочати знову за допомогою /start"
            )
            return

        # 3. Якщо спроб менше 3 — зберігаємо оновлену кількість спроб і попереджаємо
        await state.update_data(name_attempts=attempts)
        await message.answer(
            f"❌ Некоректне ім'я! Воно має містити від 2 до 25 літер.\n"
            f"⚠️ Залишилося спроб: {3 - attempts}. Спробуйте ще раз:"
        )
        return

    # Якщо ім'я правильне — зберігаємо ім'я і йдемо далі
    await state.update_data(name=name)
    await state.set_state(st.Reg.phone)
    await message.answer(
        "Дякую! Тепер надішліть свій номер телефону за допомогою кнопки нижче:",
        reply_markup=kb.request_phone
    )

# 3. Ловимо телефон (контакт) і зберігаємо юзера
@router.message(st.Reg.phone, F.contact)
async def reg_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)

    # Отримуємо всі збережені дані з FSM
    data = await state.get_data()

    # Показуємо користувачу результат
    await message.answer(
        f"Реєстрація успішна!\nІм'я: {data['name']}\nТелефон: {data['phone']}",
        reply_markup=kb.main)


    # Скидаємо стан FSM
    await state.clear()


# 1. Натискання "Записатися"
@router.message(F.text == '📝 Записатися')
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(st.BookingState.service)
    await message.answer("Оберіть послугу з переліку:", reply_markup=await kb.services_keyboard())


# 2. Вибір послуги -> Перехід до вибору майстра
@router.callback_query(st.BookingState.service, F.data.startswith('service_'))
async def select_service(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.split('_')[1])
    await state.update_data(service_id=service_id)

    await callback.answer()
    await state.set_state(st.BookingState.master)
    await callback.message.answer("Тепер оберіть майстра:", reply_markup=await kb.masters_keyboard())


# 3. Вибір майстра -> Перехід до вибору дати
@router.callback_query(st.BookingState.master, F.data.startswith('master_'))
async def select_master(callback: CallbackQuery, state: FSMContext):
    master_id = int(callback.data.split('_')[1])
    await state.update_data(master_id=master_id)

    await callback.answer()
    await state.set_state(st.BookingState.date)
    await callback.message.answer("Введіть дату та час для запису (наприклад: 20.10 15:00):")


# 4. Приймаємо дату/час від користувача, перевіряємо формат, зберігаємо у БД
@router.message(st.BookingState.date)
async def select_date(message: Message, state: FSMContext):
    user_input = message.text.strip()

    # Перевіряємо правильність формату введеної дати
    try:
        # Чекаємо формат "25.10 15:00" (день.місяць години:хвилини)
        datetime.strptime(user_input, "%d.%m %H:%M")
    except ValueError:
        # Якщо введено некоректно — показуємо підказку та не міняємо стан FSM
        await message.answer(
            "⚠️ <b>Некоректний формат дати!</b>\n\n"
            "Будь ласка, введіть дату та час за зразком: <code>20.10 15:00</code>",
            parse_mode='HTML'
        )
        return  # Зупиняємо виконання, чекаємо повторного вводу

    # Якщо формат вірний — дістаємо збережені дані з FSM
    user_data = await state.get_data()

    # Зберігаємо бронювання в базу даних (з обов'язковим await!)
    await rq.add_booking(
        tg_id=message.from_user.id,
        service_id=user_data['service_id'],
        master_id=user_data['master_id'],
        booking_date=user_input
    )

    # Повідомляємо про успіх та повертаємо головне меню
    await message.answer("✅ Вас успішно записано!", reply_markup=kb.main)
    await state.clear()


@router.message(F.text == '🗓 Мої записи')
async def show_my_bookings(message: Message):
    bookings = await rq.get_my_bookings(message.from_user.id)

    if not bookings:
        await message.answer("У вас немає активних записів.")
        return

    await message.answer("<b>Ваші записи:</b>", parse_mode='HTML')

    # Заносимо message.answer ВСЕРЕДИНУ циклу:
    for booking in bookings:
        text = f"🔹 <b>Послуга:</b> {booking.service.name}\n"
        text += f"👨‍🎨 <b>Майстер:</b> {booking.master.name}\n"
        text += f"📅 <b>Дата та час:</b> {booking.booking_date}\n"

        await message.answer(text, parse_mode='HTML',
            reply_markup=cancel_booking_kb(booking.id))


@router.message(F.text == '❕ Про нас')
async def about_us(message: Message):
    await message.answer("📍 **Наш салон:** вул. Центральна, 15\n"
        "⏰ **Графік роботи:** Щодня з 09:00 до 20:00\n"
        "📞 **Телефон:** +380991234567", parse_mode='Markdown')


@router.message(F.text == '👦 Наші майстри')
async def show_master(message: Message):
    master = await rq.get_masters()

    if not master:
        await message.answer("Список майстрів порожній!")

    text = "👦 **Наші майстри**\n\n"
    for mast in master:
        text += f"{mast.name}\n"

    await message.answer(text, parse_mode='Markdown')


@router.callback_query(F.data.startswith('cancel_'))
async def cancel_booking_handler(callback: CallbackQuery):
    booking_id = int(callback.data.split("_")[1])

    await rq.delete_booking(booking_id)

    await callback.answer("Запис скасовано!", show_alert=True)
    await callback.message.edit_text("❌ Цей запис було скасовано!")


# 1. Команда /admin — перевірка на адміна
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас немає доступу до адмін-панелі.")
        return

    await message.answer("👑 <b>Панель адміністратора:</b>", parse_mode="HTML", reply_markup=kb.admin_kb)


# 2. Перегляд усіх записів усіх клієнтів
@router.callback_query(F.data == "admin_all_bookings")
async def show_all_bookings(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    bookings = await get_all_bookings()

    if not bookings:
        await callback.message.answer("У системі немає жодного активного запису.")
        await callback.answer()
        return

    await callback.message.answer("<b>📋 Усі записи в системі:</b>", parse_mode="HTML")

    for booking in bookings:
        # Формуємо інформацію про клієнта
        user_info = f"ID: {booking.user_id}"

        text = (
            f"🆔 <b>Запис №{booking.id}</b>\n"
            f"👤 <b>Клієнт:</b> {user_info}\n"
            f"🔹 <b>Послуга:</b> {booking.service.name}\n"
            f"👨‍🎨 <b>Майстер:</b> {booking.master.name}\n"
            f"📅 <b>Дата:</b> {booking.booking_date}"
        )
        # Використовуємо ту саму функцію cancel_booking_kb, яка у нас вже є!
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=kb.cancel_booking_kb(booking.id)
        )
    await callback.answer()


# 3. Початок FSM-процесу додавання послуги
@router.callback_query(F.data == "admin_add_service")
async def start_add_service(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    await state.set_state(st.AddServiceState.name)
    await callback.message.answer("Введіть назву нової послуги (наприклад: <i>Чоловіча стрижка</i>):",
                                  parse_mode="HTML")
    await callback.answer()


# 1. Стартуємо процес додавання майстра по кліку на кнопку
@router.callback_query(F.data == "admin_add_master")
async def start_add_master(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        return

    await state.set_state(st.AddMasterState.name)
    await callback.message.answer("Введіть ім'я нового майстра:")
    await callback.answer()


# 2. Ловимо ім'я майстра, зберігаємо в БД та очищаємо стан
@router.message(st.AddMasterState.name)
async def process_master_name(message: Message, state: FSMContext):
    master_name = message.text.strip()

    # Зберігаємо в базу даних за допомогою твоєї функції
    await rq.add_master(name=master_name)
    await state.clear()

    await message.answer(f"✅ Майстра <b>{master_name}</b> успішно додано!", parse_mode="HTML")


# 4. Отримання назви послуги та запит ціни
@router.message(st.AddServiceState.name)
async def process_service_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddServiceState.price)
    await message.answer("Тепер введіть ціну послуги (тільки число, наприклад: <i>350</i>):", parse_mode="HTML")


# 5. Отримання ціни та збереження в БД
@router.message(st.AddServiceState.price)
async def process_service_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Будь ласка, введіть ціну числом (наприклад: 300)!")
        return

    data = await state.get_data()
    service_name = data["name"]
    service_price = int(message.text)

    # Зберігаємо в базу даних
    await rq.add_service(name=service_name, price=service_price)
    await state.clear()

    await message.answer(
        f"✅ Послугу <b>{service_name}</b> за <b>{service_price} грн</b> успішно додано!",
        parse_mode="HTML")