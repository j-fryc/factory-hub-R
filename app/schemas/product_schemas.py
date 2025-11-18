from typing import Optional

import uuid as uuid_pkg

from pydantic import field_validator, field_serializer

from app.schemas.base_schemas import FetchDTO, CreateDTO, UpdateDTO, DeleteDTO, OutputDTO
from app.schemas.product_type_schemas import ProductTypeFetch, ProductTypeOut


class ProductOut(OutputDTO):
    quantity: int
    price: float
    product_type_id: Optional[uuid_pkg.UUID] = None
    product_type: Optional[ProductTypeOut] = None

    @field_validator("product_type", mode="before")
    def allow_empty_dict(cls, v):
        if v == {}:
            return None
        return v

    @field_serializer("product_type")
    def serialize_empty_dict(self, v):
        return {} if v is None else v


class ProductFetch(FetchDTO):
    quantity: Optional[int] = None
    gt_price: Optional[float] = None
    lt_price: Optional[float] = None
    product_type_id: Optional[uuid_pkg.UUID] = None


class ProductCreate(CreateDTO):
    quantity: int
    price: float
    product_type_id: uuid_pkg.UUID


class ProductUpdate(UpdateDTO):
    quantity: Optional[int] = None
    price: Optional[float] = None
    product_type_id: Optional[uuid_pkg.UUID] = None


class ProductDelete(DeleteDTO):
    pass
