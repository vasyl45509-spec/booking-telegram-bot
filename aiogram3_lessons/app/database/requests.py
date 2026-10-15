# from app.database.models import async_session
# from app.database.models import User, Category, Item
# from sqlalchemy import select
#
#
# async def set_user(tg_id):
#     async with async_session () as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#     if not user:
#         session.add(User(tg_id=tg_id))
#         await session.commit()
#
#
# async def get_categories():
#     async with async_session() as session:
#         return await session.scalars(select(Category))
#
# async def get_categories_item(category_id):
#     async with async_session() as session:
#         return await session.scalars(select(Item).where(Item.category ==  category_id))
#
# async def get_item(item_id):
#     async with async_session() as session:
#         return await session.scalar(select(Item).where(Item.id ==  item_id))
from app.database.models import async_session, Basket
from app.database.models import User, Category, Item
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def set_basket(tg_id: int, item_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Basket(user=user.id, item=item_id))
        await session.commit()


async def get_basket(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        result = await session.scalars(select(Item).join(Basket,
                                                         Basket.item == Item.id).where(Basket.user == user.id))
        return result.all()

