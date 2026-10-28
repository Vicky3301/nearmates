
from app.auth import create_access_token, verify_password

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]="",
    db: Annotated[Session, Depends(get_db)]=None,
):
    # Empty password check before hitting verify_password
    if not password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.scalar(
        select(User).where(User.email == username)
    )

    if user is None or not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }