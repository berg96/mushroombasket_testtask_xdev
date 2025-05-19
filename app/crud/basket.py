from crud.base import CRUDBase
from models import Basket
from schemas.basket import BasketCreate, BasketUpdate


class CRUDBasket(CRUDBase[
    Basket,
    BasketCreate,
    BasketUpdate
]):
    pass


basket_crud = CRUDBasket(Basket)
