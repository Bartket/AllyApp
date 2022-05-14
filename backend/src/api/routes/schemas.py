from typing import List

from pydantic import BaseModel


class Point(BaseModel):
    lat: float
    lon: float


# REQUEST SCHEMAS
class RouteSchema(BaseModel):
    pass


class RouteCreateSchema(RouteSchema):
    title: str
    points: List[Point]


# RESPONSE SCHEMAS
class RouteResponseSchema(RouteSchema):
    id: int
