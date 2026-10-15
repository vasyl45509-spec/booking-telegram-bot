
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

class TestMiddleware(BaseMiddleware):
    async def __call__(self,
                       hendler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        print('Дія до оброботчика')
        result = await hendler(event, data)
        print('Дія після оброботчика')
        return result

# import time
# from aiogram import BaseMiddleware
#
#
# class ExecutionTimeMiddleware(BaseMiddleware):
#     async def __call__(self, handler, event, data):
#         start_time = time.time()  # 1. Фіксуємо час ДО хендлера
#
#         result = await handler(event, data)  # 2. Пропускаємо в хендлер
#
#         execution_time = time.time() - start_time  # 3. Рахуємо час ПІСЛЯ хендлера
#         print(f"Повідомлення оброблено за {execution_time:.4f} секунд")
#
#         return result