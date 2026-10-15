# # app/database/models.py
# from sqlalchemy import BigInteger, String, ForeignKey, DateTime
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
# from datetime import datetime
#
# engine = create_async_engine(url='sqlite+aiosqlite:///booking.sqlite3')
# async_session = async_sessionmaker(engine)
#
#
# class Base(AsyncAttrs, DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id: Mapped[int] = mapped_column(BigInteger)
#     name: Mapped[str] = mapped_column(String(50))
#     phone: Mapped[str] = mapped_column(String(20))
#
#
# class Service(Base):
#     __tablename__ = 'services'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     price: Mapped[int] = mapped_column()
#
#
# class Master(Base):
#     __tablename__ = 'masters'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#
#
# class Booking(Base):
#     __tablename__ = 'bookings'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
#     master_id: Mapped[int] = mapped_column(ForeignKey('masters.id'))
#     booking_date: Mapped[str] = mapped_column(String(30))
#
#
# async def async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# # app/database/models.py
#
# class Service(Base):
#     __tablename__ = 'services'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     price: Mapped[int] = mapped_column()
#
#
# class Master(Base):
#     __tablename__ = 'masters'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#
#
# class Booking(Base):
#     __tablename__ = 'bookings'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
#     service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
#     master_id: Mapped[int] = mapped_column(ForeignKey('masters.id'))
#     booking_date: Mapped[str] = mapped_column(String(30))
#
#     # Додаємо зв'язки з іншими таблицями
#     service: Mapped['Service'] = relationship()
#     master: Mapped['Master'] = relationship()
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///booking.sqlite3')
async_session = async_sessionmaker(engine)
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column()


class Master(Base):
    __tablename__ = 'masters'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
    master_id: Mapped[int] = mapped_column(ForeignKey('masters.id'))
    booking_date: Mapped[str] = mapped_column(String(30))

    # Зв'язки з таблицями для отримання назви послуги та майстра
    service: Mapped['Service'] = relationship()
    master: Mapped['Master'] = relationship()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)