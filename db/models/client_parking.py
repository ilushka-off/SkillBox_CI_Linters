from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .mixins import IDMixin

from datetime import datetime

if TYPE_CHECKING:
    from .client import Client
    from .parking import Parking

class ClientParking(BaseModel, IDMixin):

    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'))
    parking_id: Mapped[int] = mapped_column(Integer, ForeignKey('parkings.id'))
    time_in: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    time_out: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "parking_id",
            name="unique_client_parking"
        ),
    )

    client: Mapped["Client"] = relationship(back_populates='visits')
    parking: Mapped["Parking"] = relationship(back_populates='visitors')
