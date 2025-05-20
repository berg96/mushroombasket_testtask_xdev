import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from core.constants import (
    IS_EDIBLE_DESCRIPTION, IS_FRESH_DESCRIPTION, NAME_NOT_EMPTY
)


class MushroomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_edible: bool = Field(..., description=IS_EDIBLE_DESCRIPTION)
    weight: int = Field(..., gt=0)
    is_fresh: bool = Field(True, description=IS_FRESH_DESCRIPTION)

    @field_validator('name')
    def name_not_empty(cls, value: str) -> str:
        if value is None:
            raise ValueError(NAME_NOT_EMPTY)
        return value


class MushroomCreate(MushroomBase):
    pass


class MushroomUpdate(MushroomBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_edible: Optional[bool] = None
    weight: Optional[int] = Field(None, gt=0)
    is_fresh: Optional[bool] = None


class MushroomDB(MushroomBase):
    id: UUID
    created_at: datetime.datetime

    class Config:
        from_attributes = True
