from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.models.user import User

from app.auth.schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)
from app.auth.service import (
    register_user,
    login_user,
)
from app.core.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        result = login_user(
            db,
            user.email,
            user.password,
        )

        return {
            "access_token": result["access_token"],
            "token_type": result["token_type"],
        }

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=UserResponse,
)
def current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/logout")
def logout():
    return {
        "message": "Logged out successfully"
    }