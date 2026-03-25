import asyncio
from sqlalchemy import select
from database.models import async_session
from database.models import User

async def set_user(tg_id, steam_id = None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, steam_id = steam_id))
            await session.commit()
        else:
            if steam_id:
                user.steam_id = steam_id
                await session.commit()
        

async def get_steam_id(tg_id: int) -> str | None:
    async with async_session() as session:  
        result = await session.scalar(
            select(User.steam_id)
            .where(User.tg_id == tg_id)
        )
        return result


async def main():
    steam_id = await get_steam_id(726986137)  # Вызов с await внутри асинхронной функции
    print(f"Steam ID: {steam_id}")

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())  # Запуск ц





