from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    description: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    expense_date: date = Field(default_factory=date.today)


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    description: str
    category: str
    expense_date: date


class ExpenseListResponse(BaseModel):
    items: list[ExpenseResponse]
    page: int
    limit: int
    total: int