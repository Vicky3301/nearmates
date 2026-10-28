from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.orm import relationship

from app.models.associations import user_languages, user_interests

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    home_region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    current_city: Mapped[str | None] = mapped_column(
        String(100),
        index=True,
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    languages = relationship(
        "Language",
        secondary=user_languages,
        back_populates="users",
    )

    interests = relationship(
        "Interest",
        secondary=user_interests,
        back_populates="users",
    )