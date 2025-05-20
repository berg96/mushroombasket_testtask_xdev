from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import IS_FRESH_DESCRIPTION
from core.db import Base


class Mushroom(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_edible: Mapped[bool] = mapped_column(nullable=False, default=True)
    weight: Mapped[int] = mapped_column(nullable=False)
    is_fresh: Mapped[bool] = mapped_column(
        nullable=False, default=True, doc=IS_FRESH_DESCRIPTION
    )

    baskets: Mapped[list['Basket']] = relationship(
        secondary="mushroombaskets",
        back_populates="mushrooms",
        lazy='selectin',
    )
