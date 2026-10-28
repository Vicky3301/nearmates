from pydantic import BaseModel, ConfigDict, Field


class CatalogueItem(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PreferenceSelection(BaseModel):
    ids: list[int] = Field(
        min_length=1,
        max_length=20,
    )