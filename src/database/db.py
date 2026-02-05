from src.database.session import Base
from src.database.session import engine


async def test_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Подключение к базе установлено и таблицы проверены")
