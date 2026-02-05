# import random
# import string
# from sqlalchemy.dialects.postgresql import insert
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.database.models import Code
#
# def generate_random_code(length: int = 8) -> str:
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
#
# async def create_unique_codes(session: AsyncSession, amount: int) -> list[str]:
#     codes = set()
#     while len(codes) < amount:
#         new_codes = {generate_random_code() for _ in range(amount - len(codes))}
#
#         stmt = (
#             insert(Code)
#             .values([{"code": code, "active": True, "used": False} for code in new_codes])
#             .on_conflict_do_nothing(index_elements=["code"])
#             .returning(Code.code)
#         )
#
#         result = await session.execute(stmt)
#         inserted = [row[0] for row in result.fetchall()]  # fetchall() нужно обернуть в await
#         codes.update(inserted)
#
#     await session.commit()
#     return list(codes)
