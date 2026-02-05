from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Code


async def load_codes(session: AsyncSession) -> set[str]:
    result = await session.execute(select(Code.code))
    return {str(row[0]).strip().upper() for row in result.fetchall()}


async def check_code(session: AsyncSession, code: str) -> bool:
    normalized_code = code.strip().upper()
    stmt = select(Code).filter(Code.code == normalized_code)  # type: ignore
    result = await session.execute(stmt)
    code_obj = result.scalar_one_or_none()

    if code_obj:
        await session.delete(code_obj)
        await session.commit()
        return True
    return False


async def save_code(session: AsyncSession, code: str) -> None:
    normalized_code = code.strip().upper()
    stmt = (
        insert(Code)
        .values(code=normalized_code, active=True, used=False)
        .on_conflict_do_nothing(index_elements=["code"])
    )
    await session.execute(stmt)
    await session.commit()
