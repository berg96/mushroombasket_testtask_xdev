from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Basket(Base):
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False, default=5000)

    mushrooms: Mapped[list['Mushroom']] = relationship(
        secondary='mushroombaskets',
        back_populates='baskets',
        lazy='selectin',
    )

    @property
    def total_weight(self) -> int:
        return sum(mushroom.weight for mushroom in self.mushrooms)

    def can_add(self, mushroom: 'Mushroom') -> bool:
        return (self.total_weight + mushroom.weight) <= self.capacity


class MushroomBasket(Base):
    mushroom_id: Mapped[UUID] = mapped_column(
        ForeignKey('mushrooms.id', ondelete='CASCADE'), primary_key=True
    )
    basket_id: Mapped[UUID] = mapped_column(
        ForeignKey('baskets.id', ondelete='CASCADE'), primary_key=True
    )
