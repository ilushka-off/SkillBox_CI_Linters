from typing import Any

from pydantic import ConfigDict, BaseModel


class BaseOrmSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseKeySchema(BaseModel):
    delimiter: str
    prefix: str

    def get_key(self, *args: Any) -> str:
        return (
            f"{self.prefix}{self.delimiter}"
            f"{self.delimiter.join(str(arg) for arg in args)}"
        )
