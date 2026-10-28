from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import user_languages


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    users = relationship(
        "User",
        secondary=user_languages,
        back_populates="languages",
    )