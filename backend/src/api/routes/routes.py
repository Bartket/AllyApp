from fastapi import APIRouter

from api.routes import schemas
from api.routes.controller import Routes

router = APIRouter()


@router.post("/", response_model=schemas.RouteSchema)
async def create_route(
        data: schemas.RouteCreateSchema
) -> schemas.RouteResponseSchema:

    return Routes().create_document(data)


