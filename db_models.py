import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

# SQLAlchemy
from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, UUID, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'accounts_customuser'

    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    api_key: Mapped[str] = mapped_column(String)

    # Relationships
    orders = relationship('Orders', back_populates='user')
    watchlist = relationship('Watchlist', back_populates='user')


class Orders(Base):
    __tablename__ = 'dashboard_orders'

    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey('accounts_customuser.email'), nullable=False)
    ticker: Mapped[str] = mapped_column(String)
    dollar_amount: Mapped[float] = mapped_column(Float)
    realised_pnl: Mapped[Optional[float]] = mapped_column(Float, default=0)
    unrealised_pnl: Mapped[Optional[float]] = mapped_column(Float, default=0)
    open_price: Mapped[Optional[float]] = mapped_column(Float)
    close_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    order_type: Mapped[str] = mapped_column(String)

    # Relationships
    user = relationship("Users", back_populates="orders")


class Watchlist(Base):
    __tablename__ = 'dashboard_watchlist'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('accounts_customuser.email'))

    # Relationships
    user = relationship('Users', back_populates='watchlist')

    # Constraints
    unique_user_ticker = UniqueConstraint('ticker', 'user_id', name='unique_user_ticker')
