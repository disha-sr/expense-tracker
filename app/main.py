from fastapi import FastAPI, Request, Depends
from app.routers.budgets import router as budget_router
from app.database.database import Base, engine
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.user import User
from app.routers.expenses import router as expense_router
from app.routers.reports import router as report_router
from app.exceptions.handlers import general_exception_handler
from fastapi.responses import JSONResponse
from app.routers.auth import router as auth_router
from app.security.auth import get_current_user

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Expense Tracker API",
    description="A backend API for managing personal expenses",
    version="1.0.0"
)

@app.get("/test-token")
def test_token(
    current_user  = Depends(get_current_user)
):
    return {
            "id": current_user.id,
        "email": current_user.email
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

app.include_router(expense_router)
app.include_router(report_router)
app.include_router(budget_router)
app.include_router(auth_router)