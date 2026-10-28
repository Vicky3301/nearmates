from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


user_languages = Table(
    "user_languages",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "language_id",
        Integer,
        ForeignKey("languages.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


user_interests = Table(
    "user_interests",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "interest_id",
        Integer,
        ForeignKey("interests.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)