from typing import Sequence
from fastapi import Depends, HTTPException
from schemas.client import ClientCreateSchema


from db.models import Client
from db.repositories.client import ClientRepository


class ClientService:
    def __init__(
        self,
        client_repository: ClientRepository = Depends(),
    ):
        self._client_repository = client_repository

    async def get_all_clients(self) -> Sequence[Client]:
        return await self._client_repository.get_all_clients()

    async def get_by_id(self, id: int) -> Client:
        client = await self._client_repository.get_client_by_id(id=id)

        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        return client

    async def create_client(self, schema: ClientCreateSchema) -> Client:
        client = Client(**schema.model_dump())
        await self._client_repository.create_client(client=client)
        await self._client_repository._session.commit()
        return client
