# run.py
import asyncio

import app.database.requests as rq
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main

from config import TOKEN
# Сюди встав свій токен від BotFather

async def main():
    # Ініціалізуємо БД (створюються таблиці)
    await async_main()
    await rq.init_db_data()


    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот успішно запущений!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений.")