from datetime import datetime
from typing import Optional
from uuid import uuid4

# SQLAlchemy
from sqlalchemy import String, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# All Models were initially defined in django
# ////////////////////////////////////////////////////////

class Users(Base):
    __tablename__ = 'accounts_customuser'

    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    api_key: Mapped[str] = mapped_column(String)

    def __str__(self):
        return f"User: {self.email}"

    # Relationships
    # orders = relationship('Orders', back_populates='users')
    # watchlists = relationship('Watchlists', back_populates='users')


# class Watchlists(Base):
#     __tablename__ = 'dashboard_watchlist'
#
#     id: int = mapped_column(primary_key=True)
#     user: Users = mapped_column()
#     ticker: str = mapped_column()
#
#
# class Orders(Base):
#     __tablename__ = 'dashboard_orders'
#
#     order_id: uuid4 = mapped_column(default=uuid4, primary_key=True)
#     user: Users = mapped_column()
#     ticker: str = mapped_column()
#     dollar_amount: float = mapped_column()
#     realised_pnl: Optional[float] = mapped_column(default=0)
#     unrealised_pnl: Optional[float] = mapped_column(default=0)
#     open_price: Optional[float] = mapped_column()
#     close_price: Optional[float] = mapped_column()
#     created_at: datetime = mapped_column()
#     is_active: bool = mapped_column()
#     order_type: str = mapped_column()