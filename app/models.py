import pymongo
from beanie import Document, init_beanie
import uuid as uuid_pkg
from pydantic import Field


class ProductType(Document):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True
    )
    name: str = Field(..., description="Name of the product type")
    description: str = Field(..., description="Description of the product type")
    entity_version: int = Field(..., description="Document version")

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
    product_type_id: uuid_pkg.UUID = Field(..., description="Id of related product type")
    quantity: int = Field(..., description="Quantity of products")
    price: float = Field(..., description="Price of single product")
    entity_version: int = Field(..., description="Document version")

    class Settings:
        indexes = [
            [("name", pymongo.TEXT)]
        ]


if __name__ == "__main__":
    async def init_db(async_client):
        print(async_client.db_client.get_database())
        await init_beanie(database=async_client.db_client.get_database(), document_models=[Product, ProductType])
        ptype = ProductType(name="Book", description="Paper book")
        product = Product(name="produkt book", product_type=ptype, quantity=1, price=12.52)
        Product.find()
        await ptype.insert()
        await product.insert()
    # async_client = AsyncDatabaseClient(connection_string="mongodb://mongo:mongo@localhost:27017/test?authSource=admin")
    # async_client = AsyncDatabaseClient(connection_string="mongodb://mongo:mongo@localhost:27017")
    # asyncio.run(init_db(async_client))

    test = ProductType(**{'name': 'testtowy produkt typ', 'description': 'smoething', 'version': 1})
    print(test)