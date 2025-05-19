from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from crud.basket import basket_crud
from schemas.basket import BasketCreate, BasketDB, BasketUpdate
from uuid import UUID


router = APIRouter()


@router.post('/', response_model=BasketDB)
async def create_basket(
    data: BasketCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await basket_crud.create(data, session)


@router.get('/{basket_id}', response_model=BasketDB)
async def get_basket(
    basket_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    basket = await basket_crud.get(basket_id, session)
    if not basket:
        raise HTTPException(status_code=404, detail='Корзина не найдена')
    return basket


@router.post("/{basket_id}/add", response_model=BasketDB)
async def endpoint_add_mushroom(
    basket_id: UUID,
    data: BasketUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await basket_crud.add_mushroom(basket_id, data.mushroom_id, session)


@router.delete("/{basket_id}/remove", response_model=BasketDB)
async def endpoint_remove_mushroom(
    basket_id: UUID,
    data: BasketUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await basket_crud.remove_mushroom(
        session, basket_id, data.mushroom_id
    )
