from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.security.jwt import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.database.database import get_db
from app.models.user import User
from app.exceptions.auth import (
    InvalidTokenException,
    UserNotFoundException
)
def get_token(
    token: str = Depends(oauth2_scheme)
):
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:
        raise InvalidTokenException()

def get_current_token(
    token: str = Depends(oauth2_scheme)
):
    return verify_token(token)

def get_current_user(
    payload: dict = Depends(get_current_token),
    db = Depends(get_db)
):
    user_id = payload.get("sub")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise UserNotFoundException()

    return user