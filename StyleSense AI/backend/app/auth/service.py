from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.schemas import UserRegister
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.core.config import settings


def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def register_user(
    db: Session,
    user: UserRegister,
):
    existing_user = get_user_by_email(
        db,
        user.email,
    )

    if existing_user:
        raise ValueError("Email already registered")

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = authenticate_user(
        db,
        email,
        password,
    )

    if not user:
        raise ValueError("Invalid email or password")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        },
        expires_delta=timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }