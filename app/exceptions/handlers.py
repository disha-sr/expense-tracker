from fastapi import Request
from fastapi.responses import JSONResponse
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
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )

async def expense_not_found_handler(
    request: Request,
    exc: ExpenseNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Expense not found"
        }
    )

async def invalid_expense_request_handler(
    request: Request,
    exc: InvalidExpenseRequestException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

async def budget_not_found_handler(
    request: Request,
    exc: BudgetNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Budget not found"
        }
    )

async def duplicate_budget_handler(
    request: Request,
    exc: DuplicateBudgetException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Budget already exists for this category and month"
        }
    )

async def invalid_budget_request_handler(
    request: Request,
    exc: InvalidBudgetRequestException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

async def budget_page_not_found_handler(
    request: Request,
    exc: BudgetPageNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )

async def email_already_registered_handler(
    request: Request,
    exc: EmailAlreadyRegisteredException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Email already registered"
        }
    )

async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid email or password"
        }
    )

async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid token"
        }
    )

async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "User not found"
        }
    )