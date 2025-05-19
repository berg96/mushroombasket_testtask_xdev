from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from crud.mushroom import mushroom_crud
from schemas.mushroom import MushroomCreate, MushroomDB, MushroomUpdate

from uuid import UUID


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
    result = await mushroom_crud.get(mushroom_id, session)
    if not result:
        raise HTTPException(status_code=404, detail='Гриб не найден')
    return result


@router.put('/{mushroom_id}', response_model=MushroomDB)
async def update_mushroom(
    mushroom_id: UUID,
    data: MushroomUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    mushroom = await mushroom_crud.get(mushroom_id, session)
    if not mushroom:
        raise HTTPException(status_code=404, detail='Гриб не найден')
    return await mushroom_crud.update(mushroom, data, session)
