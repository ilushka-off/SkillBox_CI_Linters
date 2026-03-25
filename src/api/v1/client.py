from typing import Sequence

from fastapi import APIRouter, status, Depends

from db.models import Client
from schemas.client import ClientGetSchema, ClientIdGetSchema, ClientCreateSchema
from services.client import ClientService

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[ClientGetSchema])
async def get_clients(
    client_service: ClientService = Depends(),
) -> Sequence[Client]:
    return await client_service.get_all_clients()

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ClientIdGetSchema)
async def get_client(
    id: int,
    client_service: ClientService = Depends(),
) -> Client:
    return await client_service.get_by_id(id=id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ClientGetSchema)
async def create_client(
    schema: ClientCreateSchema,
    client_service: ClientService = Depends(),
) -> Client:
    return await client_service.create_client(schema)
