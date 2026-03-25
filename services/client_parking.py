from datetime import datetime, timezone
from fastapi import Depends, HTTPException

from db.models import ClientParking
from db.repositories.client import ClientRepository
from db.repositories.parking import ParkingRepository
from db.repositories.client_parking import ClientParkingRepository
from schemas.client_parking import ClientParkingCreateSchema


class ClientParkingService:
    def __init__(
        self,
        client_repo: ClientRepository = Depends(),
        parking_repo: ParkingRepository = Depends(),
        client_parking_repo: ClientParkingRepository = Depends(),
    ):
        self._client_repo = client_repo
        self._parking_repo = parking_repo
        self._client_parking_repo = client_parking_repo

    async def entry_parking(self, schema: ClientParkingCreateSchema) -> ClientParking:
        parking = await self._parking_repo.get_parking_by_id(schema.parking_id)
        if not parking:
            raise HTTPException(status_code=404, detail="Parking not found")
        if not parking.opened:
            raise HTTPException(status_code=400, detail="Parking is closed")
        if parking.count_available_places <= 0:
            raise HTTPException(status_code=400, detail="No available places")

        parking.count_available_places -= 1

        client_parking = ClientParking(
            client_id=schema.client_id,
            parking_id=schema.parking_id,
            time_in=datetime.now(timezone.utc)
        )
        await self._client_parking_repo.create_client_parking(client_parking)
        await self._client_parking_repo._session.commit()
        
        return client_parking

    async def exit_parking(self, schema: ClientParkingCreateSchema) -> ClientParking:
        client = await self._client_repo.get_client_by_id(schema.client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        if not client.credit_card:
            raise HTTPException(status_code=400, detail="Credit card not linked")

        parking = await self._parking_repo.get_parking_by_id(schema.parking_id)
        if not parking:
            raise HTTPException(status_code=404, detail="Parking not found")

        client_parking = await self._client_parking_repo.get_client_parking(schema.client_id, schema.parking_id)
        if not client_parking or client_parking.time_out is not None:
            raise HTTPException(status_code=400, detail="Client is not in this parking")

        parking.count_available_places += 1
        client_parking.time_out = datetime.now(timezone.utc)

        await self._client_parking_repo._session.commit()

        return client_parking