from typing import Sequence
from fastapi import Depends, HTTPException

from db.models import Parking
from db.repositories.parking import ParkingRepository
from schemas.parking import ParkingCreateSchema


class ParkingService:
    def __init__(
        self,
        parking_repository: ParkingRepository = Depends(),
    ):
        self._parking_repository = parking_repository

    async def get_all_parkings(self) -> Sequence[Parking]:
        return await self._parking_repository.get_all_parkings()

    async def get_by_id(self, id: int) -> Parking:
        parking = await self._parking_repository.get_parking_by_id(id=id)
        if not parking:
            raise HTTPException(status_code=404, detail="Parking not found")
        return parking

    async def create_parking(self, schema: ParkingCreateSchema) -> Parking:
        parking = Parking(**schema.model_dump())
        await self._parking_repository.create_parking(parking=parking)
        await self._parking_repository._session.commit()
        return parking
