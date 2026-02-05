from sqlalchemy import select
from src.database.models import User


async def is_admin(user_id: int, session) -> bool:
    result = await session.scalar(
        select(User.admin).where(User.tg_id == user_id)
    )
    return bool(result)
