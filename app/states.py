# app/states.py
from aiogram.fsm.state import State, StatesGroup

class Reg(StatesGroup):
    name = State()       # Стан: очікуємо введення імені
    phone = State()      # Стан: очікуємо введення телефону

class BookingState(StatesGroup):
    service = State()    # Стан: очікуємо вибір послуги
    master = State()     # Стан: очікуємо вибір майстра
    date = State()       # Стан: очікуємо вибір дати/часу

class AddServiceState(StatesGroup):
    name = State()   # Чекаємо назву послуги
    price = State()  # Чекаємо ціну

class AddMasterState(StatesGroup):
    name = State()   # Очікуємо імя нового майстра