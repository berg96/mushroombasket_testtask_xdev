from crud.base import CRUDBase
from models import Mushroom
from schemas.mushroom import MushroomCreate, MushroomUpdate


class CRUDMushroom(CRUDBase[
    Mushroom,
    MushroomCreate,
    MushroomUpdate
]):
    pass


mushroom_crud = CRUDMushroom(Mushroom)
