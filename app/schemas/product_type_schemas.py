from typing import Optional

from app.schemas.base_schemas import FetchDTO, UpdateDTO, CreateDTO, DeleteDTO, OutputDTO


class ProductTypeOut(OutputDTO):
    description: str


class ProductTypeFetch(FetchDTO):
    description: Optional[str] = None


class ProductTypeCreate(CreateDTO):
    description: str


class ProductTypeUpdate(UpdateDTO):
    description: Optional[str] = None


class ProductTypeDelete(DeleteDTO):
    pass
