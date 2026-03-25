from datetime import datetime
from schemas.base import BaseOrmSchema

class BaseClientParkingSchema(BaseOrmSchema):
    client_id: int
    parking_id: int

class ClientParkingCreateSchema(BaseClientParkingSchema):
    pass

class ClientParkingGetSchema(BaseClientParkingSchema):
    id: int
    time_in: datetime | None = None
    time_out: datetime | None = None