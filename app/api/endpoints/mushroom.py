from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import check_mushroom_exists
from core.db import get_async_session
from crud.mushroom import mushroom_crud
from schemas.mushroom import MushroomCreate, MushroomDB, MushroomUpdate

router = APIRouter()


@router.post('/', response_model=MushroomDB)
async def create_mushroom(
    data: MushroomCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await mushroom_crud.create(data, session)


@router.get('/{mushroom_id}', response_model=MushroomDB)
async def get_mushroom(
    mushroom_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    return await check_mushroom_exists(mushroom_id, session)


@router.put('/{mushroom_id}', response_model=MushroomDB)
async def update_mushroom(
    mushroom_id: UUID,
    data: MushroomUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    mushroom = await check_mushroom_exists(mushroom_id, session)
    return await mushroom_crud.update(mushroom, data, session)
