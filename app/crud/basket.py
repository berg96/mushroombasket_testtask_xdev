from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from crud.mushroom import mushroom_crud
from models import Basket
from schemas.basket import BasketCreate, BasketUpdate


class CRUDBasket(CRUDBase[
    Basket,
    BasketCreate,
    BasketUpdate
]):
    async def add_mushroom(
        self,
        basket_id: UUID,
        mushroom_id: UUID,
        session: AsyncSession,
    ) -> Basket:
        basket = await self.get(basket_id, session)
        if not basket:
            raise HTTPException(status_code=404, detail='Корзина не найдена')
        mushroom = await mushroom_crud.get(mushroom_id, session)
        if not mushroom:
            raise HTTPException(status_code=404, detail='Гриб не найден')
        if not basket.can_add(mushroom):
            raise HTTPException(status_code=400, detail='Недостаточно места в корзине')
        basket.mushrooms.append(mushroom)
        await session.commit()
        await session.refresh(basket)
        return basket

    async def remove_mushroom(
        self,
        basket_id: UUID,
        mushroom_id: UUID,
        session: AsyncSession,
    ) -> Basket:
        basket = await self.get(basket_id, session)
        if not basket:
            raise HTTPException(status_code=404, detail='Корзина не найдена')
        to_remove = next((m for m in basket.mushrooms if m.id == mushroom_id), None)
        if not to_remove:
            raise HTTPException(status_code=400, detail='Гриб не в корзине')
        basket.mushrooms.remove(to_remove)
        await session.commit()
        await session.refresh(basket)
        return basket

    async def check_mushroom_exists(
        self,
        basket_id: UUID,
        mushroom_id: UUID,
        session: AsyncSession
    ):
        basket = await self.get(basket_id, session)
        if not basket:
            raise HTTPException(status_code=404, detail='Корзина не найдена')


basket_crud = CRUDBasket(Basket)
