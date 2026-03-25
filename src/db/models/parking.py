from typing import TYPE_CHECKING, List

from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import IDMixin

if TYPE_CHECKING:
    from .client_parking import ClientParking


class Parking(BaseModel, IDMixin):

    address: Mapped[str] = mapped_column(String(length=100), nullable=False)
    opened: Mapped[bool] = mapped_column(Boolean, nullable=True)
    count_places: Mapped[int] = mapped_column(Integer, nullable=True)
    count_available_places: Mapped[int] = mapped_column(Integer, nullable=False)

    visitors: Mapped[List["ClientParking"]] = relationship(back_populates="parking")
