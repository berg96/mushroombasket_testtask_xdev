from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import Basket, Mushroom
from schemas.basket import BasketCreate, BasketUpdate


class CRUDBasket(CRUDBase[
    Basket,
    BasketCreate,
    BasketUpdate
]):
    async def add_mushroom(
        self,
        basket: Basket,
        mushroom: Mushroom,
        session: AsyncSession,
    ) -> Basket:
        basket.mushrooms.append(mushroom)
        await session.commit()
        await session.refresh(basket)
        return basket

    async def remove_mushroom(
        self,
        basket: Basket,
        mushroom_to_remove: Mushroom,
        session: AsyncSession,
    ) -> Basket:
        basket.mushrooms.remove(mushroom_to_remove)
        await session.commit()
        await session.refresh(basket)
        return basket


basket_crud = CRUDBasket(Basket)
