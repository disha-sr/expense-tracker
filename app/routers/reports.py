from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.security.auth import get_current_user
from app.database.database import get_db
from app.models.expense import Expense
from datetime import date

from app.schemas.report import (
    TotalExpenseResponse,
    MonthlyReportResponse,
    CategoryReportResponse
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get(
    "/total",
    response_model=TotalExpenseResponse
)
def get_total_expenses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    total = db.execute(
        select(func.sum(Expense.amount))
        .where(
            Expense.user_id == current_user.id
        )
    ).scalar()

    return {
        "total_expense": total or 0
    }

@router.get(
    "/monthly",
    response_model=MonthlyReportResponse
)
def get_monthly_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    total = db.execute(
        select(func.sum(Expense.amount))
        .where(
            Expense.user_id == current_user.id,
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date
        )
    ).scalar()

    return {
        "year": year,
        "month": month,
        "total_expense": total or 0
    }

@router.get(
    "/category",
    response_model=CategoryReportResponse
)
def get_category_report(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    query = (
        select(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .where(
            Expense.user_id == current_user.id,
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date
        )
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
    )

    result = db.execute(query)

    categories = [
        {
            "category": category,
            "total": total
        }
        for category, total in result.all()
    ]

    return {
        "year": year,
        "month": month,
        "categories": categories
    }