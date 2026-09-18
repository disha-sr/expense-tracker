from datetime import date
from decimal import Decimal
from app.models.expense import Expense
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func,select
from app.database.database import get_db
from app.models.budget import Budget
from app.exceptions.budget import (
    BudgetNotFoundException,
    DuplicateBudgetException,
    InvalidBudgetRequestException,
    BudgetPageNotFoundException
)
from app.schemas.budget import (
    BudgetCreate,
    BudgetResponse,
    BudgetDetailResponse,
    BudgetListResponse,
    BudgetUpdate,
    BudgetDeleteResponse
)

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

def calculate_budget_utilization(
    budget: Budget,
    db: Session
):
    start_date = date(
            budget.year,
            budget.month,
            1
        )
    
    if budget.month == 12:
        end_date = date(
            budget.year + 1,
            1,
            1
        )
    else:
        end_date = date(
            budget.year,
            budget.month + 1,
            1
        )
    spent = db.execute(
        select(func.sum(Expense.amount))
        .where(
            Expense.category == budget.category,
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date
        )
    ).scalar()
    
    spent = spent or Decimal("0")
    remaining = budget.amount - spent
    percentage_used = (spent / budget.amount) * Decimal("100")
    return {
    "spent": spent,
    "remaining": remaining,
    "percentage_used": percentage_used
}

def build_budget_response(
    budget: Budget,
    db: Session
):
    utilization = calculate_budget_utilization(budget, db)
    return {
        "id": budget.id,
        "category": budget.category,
        "amount": budget.amount,
        "month": budget.month,
        "year": budget.year,
        "spent": utilization["spent"],
        "remaining": utilization["remaining"],
        "percentage_used": utilization["percentage_used"]
    }


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=201
)
def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db)
):
    existing_budget = db.execute(
        select(Budget).where(
            Budget.category == budget.category,
            Budget.month == budget.month,
            Budget.year == budget.year
        )
    ).scalar_one_or_none()

    if existing_budget:
        raise DuplicateBudgetException()

    new_budget = Budget(
        category=budget.category,
        amount=budget.amount,
        month=budget.month,
        year=budget.year
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return build_budget_response(budget, db)

  
@router.get(
    "/",
    response_model=BudgetListResponse
)
def get_budgets(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=1),
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc"),
    db: Session = Depends(get_db)
):
    allowed_sort_fields = {
    "id": Budget.id,
    "amount": Budget.amount,
    "month": Budget.month,
    "year": Budget.year,
    "category": Budget.category,
}
    if sort_by not in allowed_sort_fields:
        raise InvalidBudgetRequestException(
            f"Invalid sort field. Allowed values: {list(allowed_sort_fields.keys())}"
    )
    if sort_order not in {"asc", "desc"}:
        raise InvalidBudgetRequestException(
            "sort_order must be 'asc' or 'desc'"
    )
    if min_amount is not None and max_amount is not None:
        if min_amount > max_amount:
            raise InvalidBudgetRequestException(
                "min_amount cannot be greater than max_amount"
    )
    query = select(Budget)
    offset = (page - 1) * limit
    if month is not None:
        query = query.where(Budget.month == month)
    if year is not None:
        query = query.where(Budget.year == year)
    if category is not None:
        query = query.where(
            func.lower(Budget.category) == category.lower()
    )
    if min_amount is not None:
        query = query.where(Budget.amount >= min_amount)
    if max_amount is not None:
        query = query.where(Budget.amount <= max_amount)
    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar() or 0
    total_pages = (total + limit - 1) // limit
    has_next = page < total_pages
    has_previous = page > 1
    
    if total_pages > 0 and page > total_pages:
        raise BudgetPageNotFoundException(
            f"Page {page} does not exist. Total pages: {total_pages}"
    )
    sort_column = allowed_sort_fields[sort_by]

    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    query = query.limit(limit).offset(offset)
    result = db.execute(query)    
    budgets = result.scalars().all()
    responses = []
   

    for budget in budgets:
        responses.append(build_budget_response(budget, db))

    return {
        "items": responses,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_previous": has_previous
    }


@router.put(
    "/{budget_id}",
    response_model=BudgetDetailResponse
)
def update_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Budget).where(Budget.id == budget_id)
    )

    budget = result.scalar_one_or_none()

    if budget is None:
        raise BudgetNotFoundException()

    # Check for duplicate category + month + year
    existing_budget = db.execute(
        select(Budget).where(
            Budget.category == budget_data.category,
            Budget.month == budget_data.month,
            Budget.year == budget_data.year,
            Budget.id != budget_id
        )
    ).scalar_one_or_none()

    if budget is None:
        raise BudgetNotFoundException()

    budget.category = budget_data.category
    budget.amount = budget_data.amount
    budget.month = budget_data.month
    budget.year = budget_data.year

    db.commit()
    db.refresh(budget)

    return build_budget_response(budget, db)

@router.get(
    "/{budget_id}",
    response_model=BudgetDetailResponse
)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Budget).where(Budget.id == budget_id)
    )

    budget = result.scalar_one_or_none()

    if budget is None:
        raise BudgetNotFoundException()

    return build_budget_response(budget, db)

@router.delete(
    "/{budget_id}",
    response_model=BudgetDeleteResponse,
    status_code=200
)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(Budget).where(Budget.id == budget_id)
    )

    budget = result.scalar_one_or_none()

    if budget is None:
        raise BudgetNotFoundException()

    db.delete(budget)
    db.commit()

    return {
    "message": "Budget deleted successfully",
    "id": budget_id
}