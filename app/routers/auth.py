from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.database.database import get_db
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.security.password import hash_password
from app.schemas.user import UserCreate, UserLogin
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    result = db.execute(
    select(User).where(User.email == user.email)
)

    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    hashed_password = hash_password(user.password)
    new_user = User(
    email=user.email,
    password_hash=hashed_password
)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
    "id": new_user.id,
    "email": new_user.email
}

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        user.password,
        existing_user.password_hash
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token({
    "sub": str(existing_user.id)
    })

    return {
    "access_token": access_token,
    "token_type": "bearer"
    }