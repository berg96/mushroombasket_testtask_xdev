from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.db import get_session
from crud.basket import basket_crud
from models.basket import Basket, MushroomBasket
from models.mushroom import Mushroom
from schemas.basket import BasketCreate, BasketDB
from uuid import UUID


router = APIRouter()


@router.post('/', response_model=BasketDB)
async def create_basket(
    data: BasketCreate,
    session: AsyncSession = Depends(get_session)
):
    return await basket_crud.create(data, session)


@router.get('/{basket_id}', response_model=BasketDB)
async def get_basket(
    basket_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    basket = await basket_crud.get(basket_id, session)
    if not basket:
        raise HTTPException(status_code=404, detail='Корзина не найдена')
    return basket


@router.post('/{basket_id}/add/{mushroom_id}', response_model=BasketDB)
async def add_mushroom_to_basket(
    basket_id: UUID,
    mushroom_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    basket = await basket_crud.get(basket_id, session)
    mushroom = await session.get(Mushroom, mushroom_id)
    if not basket or not mushroom:
        raise HTTPException(status_code=404, detail='Корзина или гриб не найдены')

    current_weight = sum(m.weight for m in basket.mushrooms)
    if current_weight + mushroom.weight > basket.capacity:
        raise HTTPException(status_code=400, detail='Превышена вместимость корзины')

    basket.mushrooms.append(mushroom)
    await session.commit()
    await session.refresh(basket)
    return basket


@router.delete('/{basket_id}/remove/{mushroom_id}', response_model=BasketDB)
async def remove_mushroom_from_basket(
    basket_id: UUID,
    mushroom_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    basket = await session.get(Basket, basket_id)
    mushroom = await session.get(Mushroom, mushroom_id)
    if not basket or not mushroom:
        raise HTTPException(status_code=404, detail='Корзина или гриб не найдены')

    if mushroom not in basket.mushrooms:
        raise HTTPException(status_code=400, detail='Гриба нет в корзине')

    basket.mushrooms.remove(mushroom)
    await session.commit()
    await session.refresh(basket)
    return basket
