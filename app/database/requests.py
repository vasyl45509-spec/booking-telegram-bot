from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.database.models import async_session, User, Service, Master, Booking


# 1. Реєстрація або перевірка користувача
async def set_user(tg_id: int, name: str = None, phone: str = None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=name, phone=phone))
            await session.commit()


# 2. Додавання початкових даних (послуги та майстри)
async def init_db_data():
    async with async_session() as session:
        services = await session.scalars(select(Service))
        if not services.first():
            session.add_all([
                Service(name="Стрижка", price=400),
                Service(name="Гоління / Борода", price=250),
                Service(name="Комплекс (Стрижка + Борода)", price=600),
            ])
            session.add_all([
                Master(name="Олександр"),
                Master(name="Михайло"),
            ])
            await session.commit()


# 3. Отримання списків для кнопок
async def get_services():
    async with async_session() as session:
        return await session.scalars(select(Service))


async def get_masters():
    async with async_session() as session:
        return await session.scalars(select(Master))


# Отримання всіх активних бронювань користувача
async def get_my_bookings(tg_id: int):
    async with async_session() as session:
        # Спочатку шукаємо користувача за його Telegram ID
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return []

        # Отримуємо всі його бронювання разом із послугою та майстром
        result = await session.scalars(
            select(Booking).where(Booking.user_id == user.id)
            .options(joinedload(Booking.service), joinedload(Booking.master)))

        return result.all()


# 4. Створення нового бронювання
async def add_booking(tg_id: int, service_id: int, master_id: int, booking_date: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        session.add(Booking(
            user_id=user.id,
            service_id=service_id,
            master_id=master_id,
            booking_date=booking_date
        ))
        await session.commit()


# Видалення бронювання за його ID
async def delete_booking(booking_id: int) -> None:
    async with async_session() as session:
        booking = await session.scalar(select(Booking).where(Booking.id == booking_id))
        if booking:
            await session.delete(booking)
            await session.commit()


# 1. Отримання ВСІХ бронювань (для адміна)
async def get_all_bookings():
    async with async_session() as session:
        result = await session.scalars(
            select(Booking)
            .options(
                joinedload(Booking.service),  # Підтягуємо послугу
                joinedload(Booking.master)    # Підтягуємо майстра
            )
        )
        return result.all()

# 2. Додавання нової послуги в базі
async def add_service(name: str, price: int):
    async with async_session() as session:
        new_service = Service(name=name, price=price)
        session.add(new_service)
        await session.commit()

async def add_master(name: str):
    async with async_session() as session:
        new_master = Master(name=name)
        session.add(new_master)
        await session.commit()
