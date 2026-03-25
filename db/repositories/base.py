from abc import ABC
from typing import TypeVar

from fastapi import Depends
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BaseModel as DBBaseModel
from db.session import get_session

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDatabaseRepository(ABC):
    _session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session
