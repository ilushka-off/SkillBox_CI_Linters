from typing import Sequence
from sqlalchemy import select
from db.models import ClientParking
from db.repositories.base import BaseDatabaseRepository

class ClientParkingRepository(BaseDatabaseRepository):
    async def create_client_parking(self, client_parking: ClientParking) -> ClientParking:
        self._session.add(client_parking)
        await self._session.flush()
        return client_parking

    async def get_client_parking(self, client_id: int, parking_id: int) -> ClientParking:
        query = select(ClientParking).where(
            ClientParking.client_id == client_id,
            ClientParking.parking_id == parking_id
        )
        query_result = await self._session.execute(query)
        return query_result.scalar()