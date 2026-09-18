from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseListResponse
)
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.expense import Expense
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.get("/", response_model=ExpenseListResponse)
def get_expenses(
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    expense_date: date | None = None,
    sort: str | None = None,
    page: int = Query(1, ge=1),
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be after end_date"
        )
    query = select(Expense).where(
    Expense.user_id == current_user.id
)

    if category:
        query = query.where(Expense.category == category)

    if min_amount is not None:
        query = query.where(Expense.amount >= min_amount)

    if max_amount is not None:
        query = query.where(Expense.amount <= max_amount)

    if expense_date is not None:
        query = query.where(Expense.expense_date == expense_date)

    if start_date is not None:
        query = query.where(Expense.expense_date >= start_date)

    if end_date is not None:
        query = query.where(Expense.expense_date <= end_date)

    if sort == "amount_asc":
        query = query.order_by(Expense.amount.asc())

    elif sort == "amount_desc":
        query = query.order_by(Expense.amount.desc())

    count_query = select(func.count()).select_from(query.subquery())

    total = db.execute(count_query).scalar()

    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    result = db.execute(query)

    expenses = result.scalars().all()

    return {
        "items": expenses,
        "page": page,
        "limit": limit,
        "total": total
    }

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = db.execute(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
    )

    expense = result.scalar_one_or_none()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense

@router.post("/", status_code=201)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_expense = Expense(
        user_id=current_user.id,
        amount=expense.amount,
        description=expense.description,
        category=expense.category,
        expense_date=expense.expense_date
        
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = db.execute(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
            )
    )

    expense = result.scalar_one_or_none()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.amount = expense_data.amount
    expense.description = expense_data.description
    expense.category = expense_data.category
    expense.expense_date = expense_data.expense_date

    db.commit()
    db.refresh(expense)

    return expense

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = db.execute(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
            )
    )

    expense = result.scalar_one_or_none()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }