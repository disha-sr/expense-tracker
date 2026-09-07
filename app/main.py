from fastapi import FastAPI, Request
from app.routers.budgets import router as budget_router
from app.database.database import Base, engine
from app.models.expense import Expense
from app.models.budget import Budget
from app.routers.expenses import router as expense_router
from app.routers.reports import router as report_router
from app.exceptions.handlers import general_exception_handler
from fastapi.responses import JSONResponse
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Expense Tracker API",
    description="A backend API for managing personal expenses",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

app.include_router(expense_router)
app.include_router(report_router)
app.include_router(budget_router)