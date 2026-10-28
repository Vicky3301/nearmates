from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas.discovery import DiscoveryResponse
from app.services.discovery import discover_users


router = APIRouter(
    tags=["Discovery"],
)


@router.get(
    "/discover",
    response_model=DiscoveryResponse,
)
def get_discoveries(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=50)] = 10,
):
    return discover_users(
        db=db,
        current_user=current_user,
        page=page,
        page_size=page_size,
    )