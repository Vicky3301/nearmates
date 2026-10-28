from sqlalchemy import text
from app.database import engine
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.security import hash_password
from app.routers.auth import router as auth_router
from app.routers.catalogue import router as catalogue_router
from app.routers.preferences import router as preferences_router
from typing import Annotated
from app.routers.discovery import router as discovery_router
from fastapi import Depends
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
app = FastAPI(
    title="NearMates API",
    description="Find people who share your language and interests.",
    version="0.1.0",
)
app.include_router(auth_router)
app.include_router(catalogue_router)
app.include_router(preferences_router)
app.include_router(discovery_router)
@app.get("/")
def root():
    return {
        "message": "Welcome to NearMates!",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        # Check whether the email is already registered.
        existing_user = db.scalar(
            select(User).where(User.email == user_data.email)
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered.",
            )

        # Hash the password before storing it.
        hashed_password = hash_password(user_data.password)

        # Create a SQLAlchemy User object.
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            home_region=user_data.home_region,
            current_city=user_data.current_city,
            bio=user_data.bio,
        )

        # Add the object to the current transaction.
        db.add(new_user)

        # Save the transaction to PostgreSQL.
        db.commit()

        # Retrieve database-generated values such as id and created_at.
        db.refresh(new_user)

        return new_user

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A conflicting user record already exists.",
        ) from None

    except Exception:
        db.rollback()
        raise

@app.get(
    "/users/me",
    response_model=UserResponse,
)
def read_current_user(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return current_user