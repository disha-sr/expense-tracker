from pydantic import BaseModel


class TotalExpenseResponse(BaseModel):
    total_expense: float


class MonthlyReportResponse(BaseModel):
    year: int
    month: int
    total_expense: float


class CategoryTotal(BaseModel):
    category: str
    total: float


class CategoryReportResponse(BaseModel):
    year: int
    month: int
    categories: list[CategoryTotal]