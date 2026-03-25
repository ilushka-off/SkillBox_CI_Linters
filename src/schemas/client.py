from schemas.base import BaseOrmSchema


class BaseClientSchema(BaseOrmSchema):
    name: str
    surname: str
    credit_card: str | None
    car_number: str | None


class ClientCreateSchema(BaseClientSchema):
    pass


class ClientGetSchema(BaseClientSchema):
    id: int


class ClientIdGetSchema(BaseClientSchema):
    id: int
