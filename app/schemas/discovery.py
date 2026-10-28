from pydantic import BaseModel, Field


class DiscoveryUser(BaseModel):
    user_id: int
    username: str
    home_region: str | None
    current_city: str | None
    bio: str | None

    shared_languages: list[str]
    shared_interests: list[str]

    match_score: float


class DiscoveryResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: list[DiscoveryUser]


class DiscoveryQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)