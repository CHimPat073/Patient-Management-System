from sqlalchemy import Float, Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    pass

class Patient(Base):

    __tablename__ = "patient_db"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(20))
    height: Mapped[float] = mapped_column(Float)  # centimeters
    weight: Mapped[float] = mapped_column(Float)  # kilograms
    diagnosis: Mapped[str] = mapped_column(String(100))
    last_visit: Mapped[date] = mapped_column(Date)
