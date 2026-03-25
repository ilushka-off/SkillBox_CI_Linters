from typing import Sequence, Any

from sqlalchemy import select, delete, Result
from db.models import Client
from db.repositories.base import BaseDatabaseRepository



class ClientRepository(BaseDatabaseRepository):
    async def get_all_clients(self) -> Sequence[Client]:
        query = select(Client)
        query_result = await self._session.execute(query)
        return query_result.scalars().all()

    async def get_client_by_id(self, id: int) -> Client:
        query = select(Client).where(Client.id == id)
        query_result = await self._session.execute(query)
        return query_result.scalar()

    async def create_client(self, client: Client) -> Client:
        self._session.add(client)
        await self._session.flush()
        return client