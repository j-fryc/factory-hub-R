from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import uuid as uuid_pkg

from app.r_services.product_service import ProductService, get_product_service
from app.r_services.product_type_service import get_product_type_service, ProductTypeService
from app.r_services.services_exceptions import DBException
from app.repositories.repositories_exceptions import NotFoundError
from app.schemas.product_schemas import ProductFetch
from app.schemas.product_type_schemas import ProductTypeFetch

r_router = APIRouter(prefix="/api/v1/r")


@r_router.get("/products/")
async def get_product_list(
        product_filters: ProductFetch = Depends(),
        product_service: ProductService = Depends(get_product_service)
):
    try:
        data = await product_service.fetch(filter_data=product_filters)
        json_compatible_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@r_router.get("/product/{product_id}")
async def get_product(
        product_id: uuid_pkg.UUID,
        product_service: ProductService = Depends(get_product_service)
):
    try:
        data = await product_service.fetch_single_record(reference_id=product_id)
        json_compatible_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@r_router.get("/product-types/")
async def get_product_type_list(
        product_type_filter: ProductTypeFetch = Depends(),
        product_type_service: ProductTypeService = Depends(get_product_type_service)
):
    try:
        data = await product_type_service.fetch(filter_data=product_type_filter)
        json_compatible_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@r_router.get("/product-type/{product_type_id}")
async def get_product_type(
        product_type_id: uuid_pkg.UUID,
        product_typ_service: ProductTypeService = Depends(get_product_type_service)
):
    try:
        data = await product_typ_service.fetch_single_record(reference_id=product_type_id)
        json_compatible_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_data)
    except (ValidationError, NotFoundError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except DBException as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
