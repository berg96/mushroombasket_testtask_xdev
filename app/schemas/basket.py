import datetime
from uuid import UUID

from pydantic import BaseModel


class BasketBase(BaseModel):
    pass


class BasketCreate(BasketBase):
    pass


class BasketUpdate(BasketBase):
    pass


class BasketDB(BasketBase):
    id: UUID
    created_at: datetime.datetime

    class Config:
        orm_mode = True
