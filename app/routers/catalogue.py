from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Interest, Language
from app.schemas.catalogue import CatalogueItem


router = APIRouter(
    tags=["Catalogue"],
)


@router.get(
    "/languages",
    response_model=list[CatalogueItem],
)
def list_languages(
    db: Annotated[Session, Depends(get_db)],
):
    return db.scalars(
        select(Language).order_by(Language.name)
    ).all()


@router.get(
    "/interests",
    response_model=list[CatalogueItem],
)
def list_interests(
    db: Annotated[Session, Depends(get_db)],
):
    return db.scalars(
        select(Interest).order_by(Interest.name)
    ).all()