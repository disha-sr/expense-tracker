from decimal import Decimal

from sqlalchemy import Numeric,Column, Integer, Float, String, Date

from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    expense_date = Column(Date, nullable=False)