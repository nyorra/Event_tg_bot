from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


# ------------------ USERS ------------------


async def is_user_exists(session: AsyncSession, tg_id: int) -> bool:
    result = await session.execute(select(User.tg_id).where(User.tg_id == tg_id))
    return result.scalar_one_or_none() is not None


async def create_user(
    session: AsyncSession, username: str, phone: str, tg_id: int
) -> None:
    stmt = (
        insert(User)
        .values(
            username=username,
            phone=phone,
            tg_id=tg_id,
            points=0,
            cup=0,
            ban_until=None,
            quiz_history=[],
            coffee_attempts=0,
        )
        .on_conflict_do_nothing(index_elements=["tg_id"])
    )
    await session.execute(stmt)
    await session.commit()


async def get_user_points(session: AsyncSession, tg_id: int) -> int:
    result = await session.execute(select(User.points).where(User.tg_id == tg_id))
    points = result.scalar_one_or_none()
    return points if points is not None else 0


async def get_user(session: AsyncSession, tg_id: int) -> Optional[Dict]:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()
    return user.__dict__ if user else None


# ------------------ POINTS & CUPS ------------------


async def increment_points(session: AsyncSession, tg_id: int, amount: int = 1) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(points=User.points + amount)
    await session.execute(stmt)
    await session.commit()


async def decrement_points(session: AsyncSession, tg_id: int, amount: int = 1) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(points=User.points - amount)
    await session.execute(stmt)
    await session.commit()


async def set_user_points(session: AsyncSession, tg_id: int, points: int) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(points=points)
    await session.execute(stmt)
    await session.commit()


async def increment_cup(session: AsyncSession, tg_id: int, amount: int = 1) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(cup=User.cup + amount)
    await session.execute(stmt)
    await session.commit()


# ------------------ BAN USERS ------------------


async def set_ban(session: AsyncSession, tg_id: int, days: int = 1) -> None:
    ban_until = datetime.now(timezone.utc) + timedelta(days=days)
    stmt = update(User).where(User.tg_id == tg_id).values(ban_until=ban_until)
    await session.execute(stmt)
    await session.commit()


async def set_ban_until(session: AsyncSession, tg_id: int, ban_until: datetime) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(ban_until=ban_until)
    await session.execute(stmt)
    await session.commit()


async def is_banned(session: AsyncSession, tg_id: int) -> bool:
    result = await session.execute(select(User.ban_until).where(User.tg_id == tg_id))
    ban_until = result.scalar_one_or_none()
    if not ban_until:
        return False
    if ban_until.tzinfo is None:
        ban_until = ban_until.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) < ban_until


async def remove_ban(session: AsyncSession, tg_id: int) -> None:
    stmt = update(User).where(User.tg_id == tg_id).values(ban_until=None)
    await session.execute(stmt)
    await session.commit()


# ------------------ QUIZ HISTORY ------------------


async def has_user_completed_quiz(
    session: AsyncSession, tg_id: int, week_number: int
) -> bool:
    result = await session.execute(select(User.quiz_history).where(User.tg_id == tg_id))
    quiz_history = result.scalar_one_or_none() or []
    return week_number in quiz_history


async def complete_quiz(session: AsyncSession, tg_id: int, week_number: int) -> None:
    result = await session.execute(select(User.quiz_history).where(User.tg_id == tg_id))
    quiz_history: List[int] = result.scalar_one_or_none() or []

    if week_number not in quiz_history:
        quiz_history.append(week_number)
        stmt = update(User).where(User.tg_id == tg_id).values(quiz_history=quiz_history)
        await session.execute(stmt)
        await session.commit()
