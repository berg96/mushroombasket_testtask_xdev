import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.mushroom import MushroomDB


class BasketBase(BaseModel):
    pass


class BasketCreate(BasketBase):
    owner: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., gt=0)


class BasketUpdate(BasketBase):
    mushroom_id: UUID = Field(...)


class BasketDB(BasketCreate):
    id: UUID
    created_at: datetime.datetime
    mushrooms: list[MushroomDB] = Field(
        default_factory=list, description='Список грибов в корзине'
    )

    class Config:
        from_attributes = True
