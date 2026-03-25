from fastapi import APIRouter, status, Depends

from db.models import Parking
from schemas.parking import ParkingCreateSchema, ParkingGetSchema
from services.parking import ParkingService

router = APIRouter(prefix="/parkings", tags=["Parkings"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ParkingGetSchema)
async def create_parking(
    schema: ParkingCreateSchema,
    parking_service: ParkingService = Depends(),
) -> Parking:
    return await parking_service.create_parking(schema)
