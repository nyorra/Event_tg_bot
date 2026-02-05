from datetime import datetime
from typing import List, Optional

from sqlalchemy import BigInteger, Integer, Text, DateTime, ARRAY, TIMESTAMP, func
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database.session import Base


class Code(Base):
    __tablename__ = "codes"

    code = Column(String, primary_key=True, index=True)
    active = Column(Boolean, default=True, nullable=False)
    used = Column(Boolean, default=False, nullable=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cup: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ban_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    quiz_history: Mapped[List[int]] = mapped_column(ARRAY(Integer), default=[])
    coffee_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)



class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    file_id = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    status = Column(String, default="pending", nullable=False)
    checked_by = Column(BigInteger, nullable=True)
    checked_at = Column(TIMESTAMP(timezone=True), nullable=True)
