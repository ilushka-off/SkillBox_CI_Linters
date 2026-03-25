from schemas.base import BaseOrmSchema


class BaseParkingSchema(BaseOrmSchema):
    address: str
    opened: bool | None = None
    count_places: int | None = None
    count_available_places: int


class ParkingCreateSchema(BaseParkingSchema):
    pass


class ParkingGetSchema(BaseParkingSchema):
    id: int
