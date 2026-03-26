from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DATE, DECIMAL, TEXT, TIMESTAMP, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)
    account_balance: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 2), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
