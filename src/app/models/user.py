from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.patient import Base


class User(Base):

	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	username: Mapped[str] = mapped_column(String(100), unique=True,nullable=False)
	password_hash: Mapped[str] = mapped_column(String(255),nullable=False)
	role: Mapped[str] = mapped_column(String(50),nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime,nullable=False)
