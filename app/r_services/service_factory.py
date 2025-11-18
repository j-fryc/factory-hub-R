from app.r_services.product_service import ProductService
from app.r_services.product_type_service import ProductTypeService
from app.repositories.product_repository import ProductRepository
from app.repositories.product_type_repository import ProductTypeRepository
from app.schemas.db_sync_schema import WorkerTypes, WorkerTypeValue


class ServiceFactory:
    @classmethod
    def create_service(cls, worker_type: WorkerTypeValue):
        match worker_type:
            case WorkerTypes.Product:
                return ProductService(repository=ProductRepository())
            case WorkerTypes.ProductType:
                return ProductTypeService(repository=ProductTypeRepository())
            case _:
                raise ValueError(f"Unknown worker type: {worker_type}")
