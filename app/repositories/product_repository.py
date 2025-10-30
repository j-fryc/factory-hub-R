from app.models import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)


def get_product_repository() -> ProductRepository:
    return ProductRepository()
