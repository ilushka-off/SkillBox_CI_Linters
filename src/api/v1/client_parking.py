from fastapi import APIRouter, status, Depends

from db.models import ClientParking
from schemas.client_parking import ClientParkingCreateSchema, ClientParkingGetSchema
from services.client_parking import ClientParkingService

router = APIRouter(prefix="/client_parkings", tags=["Client Parkings"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ClientParkingGetSchema
)
async def entry_parking(
    schema: ClientParkingCreateSchema,
    client_parking_service: ClientParkingService = Depends(),
) -> ClientParking:
    return await client_parking_service.entry_parking(schema)


@router.delete(
    "", status_code=status.HTTP_200_OK, response_model=ClientParkingGetSchema
)
async def exit_parking(
    schema: ClientParkingCreateSchema,
    client_parking_service: ClientParkingService = Depends(),
) -> ClientParking:
    return await client_parking_service.exit_parking(schema)
