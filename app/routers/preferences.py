from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Interest, Language, User
from app.schemas.catalogue import (
    CatalogueItem,
    PreferenceSelection,
)


router = APIRouter(
    prefix="/users/me",
    tags=["Preferences"],
)


@router.put(
    "/languages",
    response_model=list[CatalogueItem],
)
def update_languages(
    selection: PreferenceSelection,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    if len(selection.ids) != len(set(selection.ids)):
        raise HTTPException(
            status_code=422,
            detail="Duplicate language IDs are not allowed.",
        )

    languages = db.scalars(
        select(Language).where(
            Language.id.in_(selection.ids)
        )
    ).all()

    if len(languages) != len(selection.ids):
        raise HTTPException(
            status_code=422,
            detail="One or more language IDs do not exist.",
        )

    try:
        current_user.languages = languages

        db.commit()

        return sorted(
            current_user.languages,
            key=lambda language: language.name,
        )

    except Exception:
        db.rollback()
        raise


@router.get(
    "/languages",
    response_model=list[CatalogueItem],
)
def get_my_languages(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return sorted(
        current_user.languages,
        key=lambda language: language.name,
    )

@router.put(
    "/interests",
    response_model=list[CatalogueItem],
)
def update_interests(
    selection: PreferenceSelection,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    if len(selection.ids) != len(set(selection.ids)):
        raise HTTPException(
            status_code=422,
            detail="Duplicate interest IDs are not allowed.",
        )

    interests = db.scalars(
        select(Interest).where(
            Interest.id.in_(selection.ids)
        )
    ).all()

    if len(interests) != len(selection.ids):
        raise HTTPException(
            status_code=422,
            detail="One or more interest IDs do not exist.",
        )

    try:
        current_user.interests = interests

        db.commit()

        return sorted(
            current_user.interests,
            key=lambda interest: interest.name,
        )

    except Exception:
        db.rollback()
        raise


@router.get(
    "/interests",
    response_model=list[CatalogueItem],
)
def get_my_interests(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return sorted(
        current_user.interests,
        key=lambda interest: interest.name,
    )