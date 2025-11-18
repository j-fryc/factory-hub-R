from typing import Optional

from pydantic import BaseModel, ConfigDict
import uuid as uuid_pkg


class OutputDTO(BaseModel):
    id: uuid_pkg.UUID
    name: str
    entity_version: int

    model_config = ConfigDict(from_attributes=True)


class FetchDTO(BaseModel):
    name: Optional[str] = None


class CreateDTO(BaseModel):
    name: str
    entity_version: int


class UpdateDTO(BaseModel):
    id: uuid_pkg.UUID
    name: Optional[str] = None
    entity_version: int


class DeleteDTO(BaseModel):
    id: uuid_pkg.UUID
    entity_version: int
