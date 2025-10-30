from typing import Optional

from sqlmodel import SQLModel
from pydantic import ConfigDict, BaseModel
import uuid as uuid_pkg


class ProductTypeOut(BaseModel):
    id: uuid_pkg.UUID
    type_name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ProductTypeIn(BaseModel):
    id: Optional[uuid_pkg.UUID] = None
    type_name: Optional[str] = None
    description: Optional[str] = None
