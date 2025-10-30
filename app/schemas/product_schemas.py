from typing import Optional

from pydantic import ConfigDict, BaseModel
import uuid as uuid_pkg

from app.schemas.product_type_schemas import ProductTypeOut, ProductTypeIn


class ProductIn(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    gt_price: Optional[float] = None
    lt_price: Optional[float] = None
    product_type: Optional[ProductTypeIn] = None


class ProductOut(BaseModel):
    id: uuid_pkg.UUID
    name: str
    quantity: int
    price: float
    product_type: ProductTypeOut

    model_config = ConfigDict(from_attributes=True)
