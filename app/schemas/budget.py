from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    category: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000)


class BudgetResponse(BaseModel):
    id: int
    category: str
    amount: Decimal
    month: int
    year: int
    spent: Decimal
    remaining: Decimal
    percentage_used: Decimal
    model_config = ConfigDict(from_attributes=True)

class BudgetDetailResponse(BaseModel):
    id: int
    category: str
    amount: Decimal
    month: int
    year: int
    spent: Decimal
    remaining: Decimal
    percentage_used: Decimal

class BudgetListResponse(BaseModel):
    items: list[BudgetDetailResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

class BudgetUpdate(BaseModel):
    category: str = Field(min_length=1)
    amount: Decimal = Field(gt = 0)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000)

class BudgetDeleteResponse(BaseModel):
    message: str
    id: int