from enum import Enum, StrEnum
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict

from app.schemas.product_schemas import ProductUpdate, ProductCreate, ProductDelete
from app.schemas.product_type_schemas import ProductTypeUpdate, ProductTypeCreate, ProductTypeDelete


class AggregateType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class OutboxEventDTO(BaseModel):
    event_type: AggregateType
    payload: Union[
        ProductCreate,
        ProductUpdate,
        ProductDelete,
        ProductTypeCreate,
        ProductTypeUpdate,
        ProductTypeDelete,
    ]

    model_config = ConfigDict(from_attributes=True)


class WorkerTypes(StrEnum):
    Product = 'product'
    ProductType = 'producttype'


WorkerTypeValue = Literal[tuple(member.value for member in WorkerTypes)]
