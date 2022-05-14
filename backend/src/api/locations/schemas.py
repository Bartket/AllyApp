from pydantic import BaseModel


# REQUEST SCHEMAS
class LocationSchema(BaseModel):
    pass


class LocationCreateSchema(LocationSchema):
    title: str
    lat: float
    lon: float
    tags: str


# RESPONSE SCHEMAS
class LocationResponseSchema(LocationSchema):
    id: int
