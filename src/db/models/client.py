from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel
from .mixins import IDMixin

if TYPE_CHECKING:
    from .client_parking import ClientParking


class Client(BaseModel, IDMixin):

    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    surname: Mapped[str] = mapped_column(String(length=50), nullable=False)
    credit_card: Mapped[str] = mapped_column(String(length=50), nullable=True)
    car_number: Mapped[str] = mapped_column(String(length=50), nullable=True)

    visits: Mapped[List["ClientParking"]] = relationship(back_populates="client")

