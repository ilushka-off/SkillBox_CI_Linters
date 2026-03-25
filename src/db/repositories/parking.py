from typing import Sequence
from sqlalchemy import select
from db.models import Parking
from db.repositories.base import BaseDatabaseRepository


class ParkingRepository(BaseDatabaseRepository):
    async def get_all_parkings(self) -> Sequence[Parking]:
        query = select(Parking)
        query_result = await self._session.execute(query)
        return query_result.scalars().all()

    async def get_parking_by_id(self, id: int) -> Parking | None:
        query = select(Parking).where(Parking.id == id)
        query_result = await self._session.execute(query)
        return query_result.scalar()

    async def create_parking(self, parking: Parking) -> Parking:
        self._session.add(parking)
        await self._session.flush()
        return parking
