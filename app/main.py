from fastapi import FastAPI, Depends

from app.routers.budgets import router as budget_router
from app.database.database import Base, engine
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.user import User
from app.routers.expenses import router as expense_router
from app.routers.reports import router as report_router
from app.routers.auth import router as auth_router
from app.security.auth import get_current_user

from app.exceptions.expense import (
    ExpenseNotFoundException,
    InvalidExpenseRequestException
)

from app.exceptions.budget import (
    BudgetNotFoundException,
    DuplicateBudgetException,
    InvalidBudgetRequestException,
    BudgetPageNotFoundException
)

from app.exceptions.auth import (
    EmailAlreadyRegisteredException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException
)

from app.exceptions.handlers import (
    general_exception_handler,
    expense_not_found_handler,
    invalid_expense_request_handler,
    budget_not_found_handler,
    duplicate_budget_handler,
    invalid_budget_request_handler,
    budget_page_not_found_handler,
    email_already_registered_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    user_not_found_handler
)

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Expense Tracker API",
    description="A backend API for managing personal expenses",
    version="1.0.0"
)


@app.get("/test-token")
def test_token(
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }


app.add_exception_handler(
    Exception,
    general_exception_handler
)

app.add_exception_handler(
    ExpenseNotFoundException,
    expense_not_found_handler
)

app.add_exception_handler(
    InvalidExpenseRequestException,
    invalid_expense_request_handler
)

app.add_exception_handler(
    BudgetNotFoundException,
    budget_not_found_handler
)

app.add_exception_handler(
    DuplicateBudgetException,
    duplicate_budget_handler
)

app.add_exception_handler(
    InvalidBudgetRequestException,
    invalid_budget_request_handler
)

app.add_exception_handler(
    BudgetPageNotFoundException,
    budget_page_not_found_handler
)

app.add_exception_handler(
    EmailAlreadyRegisteredException,
    email_already_registered_handler
)

app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_handler
)

app.add_exception_handler(
    InvalidTokenException,
    invalid_token_handler
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler
)


app.include_router(expense_router)
app.include_router(report_router)
app.include_router(budget_router)
app.include_router(auth_router)