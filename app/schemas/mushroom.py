import datetime
from uuid import UUID

from pydantic import BaseModel


class MushroomBase(BaseModel):
    pass


class MushroomCreate(MushroomBase):
    pass


class MushroomUpdate(MushroomBase):
    pass


class MushroomDB(MushroomBase):
    id: UUID
    created_at: datetime.datetime

    class Config:
        orm_mode = True
