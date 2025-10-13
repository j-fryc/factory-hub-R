from fastapi import APIRouter

r_router = APIRouter(prefix="/api/v1/r")


@r_router.get("/products/")
async def get_product_list(
):
    pass


@r_router.get("/product/{product_id}")
async def get_product(
        product_id: str,
):
    pass


@r_router.get("/product-types/")
async def get_product_type_list(
):
    pass


@r_router.get("/product-type/{product_type_id}")
async def get_product_type(
        product_type_id: str,
):
    pass