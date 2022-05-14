from fastapi import APIRouter

from api.locations import schemas
from api.locations.controller import Locations

router = APIRouter()


@router.post("/", response_model=schemas.LocationSchema)
def create_location(
        data: schemas.LocationCreateSchema
) -> schemas.LocationSchema:

    return Locations.create_document(data)


