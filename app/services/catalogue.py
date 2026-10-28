from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Interest, Language


DEFAULT_LANGUAGES = [
    "Marathi",
    "Hindi",
    "English",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Gujarati",
    "Punjabi",
    "Urdu",
    "Odia",
]


DEFAULT_INTERESTS = [
    "Cricket",
    "Football",
    "Trekking",
    "Gaming",
    "Photography",
    "Music",
    "Movies",
    "Reading",
    "Technology",
    "Fitness",
    "Cooking",
    "Travel",
    "Chess",
    "Board Games",
]


def seed_catalogue(db: Session) -> None:
    for language_name in DEFAULT_LANGUAGES:
        existing_language = db.scalar(
            select(Language).where(
                Language.name == language_name
            )
        )

        if existing_language is None:
            db.add(Language(name=language_name))

    for interest_name in DEFAULT_INTERESTS:
        existing_interest = db.scalar(
            select(Interest).where(
                Interest.name == interest_name
            )
        )

        if existing_interest is None:
            db.add(Interest(name=interest_name))

    db.commit()