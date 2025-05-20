from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import BASKET_NOT_FOUND, MUSHROOM_NOT_FOUND
from crud.basket import basket_crud
from crud.mushroom import mushroom_crud
from models import Basket, Mushroom


async def check_basket_exists(
    basket_id: UUID,
    session: AsyncSession,
) -> Basket:
    basket = await basket_crud.get(basket_id, session)
    if not basket:
        raise HTTPException(
            status_code=404, detail=BASKET_NOT_FOUND.format(basket_id)
        )
    return basket


async def check_mushroom_exists(
    mushroom_id: UUID,
    session: AsyncSession,
) -> Mushroom:
    mushroom = await mushroom_crud.get(mushroom_id, session)
    if not mushroom:
        raise HTTPException(
            status_code=404, detail=MUSHROOM_NOT_FOUND.format(mushroom_id)
        )
    return mushroom
