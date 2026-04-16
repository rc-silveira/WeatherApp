from datetime import datetime
from sqlalchemy import DateTime, Float, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(30))
    temperature: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(150))
    humidity: Mapped[float] = mapped_column(Float)
    forecast_datetime: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"Weather(id={self.id!r}, city={self.city!r}, temp={self.temperature!r})"

class City(Base):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"City(id={self.id!r}, name={self.name!r})"
