import asyncio
from typing import Optional

import pymongo
from beanie import Document, Link, BackLink, init_beanie
import uuid as uuid_pkg
from pydantic import Field

from app.db_handler.async_db_handler import AsyncDatabaseClient


class ProductType(Document):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True
    )
    type_name: str = Field(..., description="Name of the product type")
    description: str = Field(..., description="Description of the product type")
    products: Optional[BackLink["Product"]] = Field(json_schema_extra={"original_field": "product_type"})

    class Settings:
        indexes = [
            [("description", pymongo.TEXT)]
        ]


class Product(Document):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True
    )
    name: str = Field(..., description="Name of the product")
    product_type: Link[ProductType]
    quantity: int = Field(..., description="Quantity of products")
    price: float = Field(..., description="Price of single product")

    class Settings:
        indexes = [
            [("name", pymongo.TEXT)]
        ]


async def init_db(async_client):
    print(async_client.db_client.get_database())
    await init_beanie(database=async_client.db_client.get_database(), document_models=[Product, ProductType])
    ptype = ProductType(type_name="Book", description="Paper book")
    product = Product(name="produkt book", product_type=ptype, quantity=1, price=12.52)
    Product.find()
    await ptype.insert()
    await product.insert()


if __name__ == "__main__":
    async_client = AsyncDatabaseClient(connection_string="mongodb://mongo:mongo@localhost:27017/test?authSource=admin")
    # async_client = AsyncDatabaseClient(connection_string="mongodb://mongo:mongo@localhost:27017")
    asyncio.run(init_db(async_client))