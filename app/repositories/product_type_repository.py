from app.models import ProductType
from app.repositories.base import BaseRepository


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self):
        super().__init__(ProductType)


def get_product_type_repository() -> ProductTypeRepository:
    return ProductTypeRepository()
