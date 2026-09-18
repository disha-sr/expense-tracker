from decimal import Decimal
from sqlalchemy import Numeric
from sqlalchemy import Integer, String, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, UniqueConstraint, Numeric, ForeignKey
from app.database.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category",
            "month",
            "year",
            name="uq_budget_user_category_month_year"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    month: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )