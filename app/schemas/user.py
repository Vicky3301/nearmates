from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    home_region: str | None = Field(
        default=None,
        max_length=100,
    )

    current_city: str | None = Field(
        default=None,
        max_length=100,
    )

    bio: str | None = Field(
        default=None,
        max_length=500,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    home_region: str | None
    current_city: str | None
    bio: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)