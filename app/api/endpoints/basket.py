from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import check_basket_exists, check_mushroom_exists
from core.constants import (
    MUSHROOM_IS_NOT_IN_BASKET, NOT_ENOUGH_SPACE_IN_BASKET
)
from core.db import get_async_session
from crud.basket import basket_crud
from models import Basket, Mushroom
from schemas.basket import BasketCreate, BasketDB, BasketUpdate

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
    return await check_basket_exists(basket_id, session)


@router.post("/{basket_id}/add", response_model=BasketDB)
async def add_mushroom(
    basket_id: UUID,
    data: BasketUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    basket = await check_basket_exists(basket_id, session)
    mushroom = await check_mushroom_exists(data.mushroom_id, session)
    if not basket.can_add(mushroom):
        raise HTTPException(
            status_code=400,
            detail=NOT_ENOUGH_SPACE_IN_BASKET.format(basket_id)
        )
    return await basket_crud.add_mushroom(basket, mushroom, session)


@router.delete("/{basket_id}/remove", response_model=BasketDB)
async def remove_mushroom(
    basket_id: UUID,
    data: BasketUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    basket = await check_basket_exists(basket_id, session)
    mushroom_to_remove = (await session.execute(
        select(Mushroom).join(Basket.mushrooms).where(
            Basket.id == basket_id,
            Mushroom.id == data.mushroom_id
        )
    )).scalar_one_or_none()
    if not mushroom_to_remove:
        raise HTTPException(
            status_code=400,
            detail=MUSHROOM_IS_NOT_IN_BASKET.format(
                data.mushroom_id, basket_id
            )
        )
    return await basket_crud.remove_mushroom(
        basket, mushroom_to_remove, session
    )
