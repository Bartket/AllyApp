import uuid
from typing import Optional, Tuple

from config.db import db
from .schemas import RouteCreateSchema


class Routes:

    def create_document(
            self, route: RouteCreateSchema, route_id: Optional[str] = None
    ):
        result = self.get_document_by_title(
            route.title
        )
        if result is None:
            if route_id is None:
                route_id = str(uuid.uuid4())

            document = db.db.collection('routes').document(route_id)
            document.set(route.dict())
            return {'id': route_id}
        else:
            route_to_update, existing_route_id = result
            document = db.db.collection('routes').document(existing_route_id)
            route_to_update.points.extend(route.points)
            document.update(route_to_update.dict())
            return {'id': existing_route_id}

    @staticmethod
    def get_document_by_title(route_title: str) -> Optional[Tuple]:
        collection = db.db.collection("routes")
        routes = collection.stream()
        for route in routes:
            if route.to_dict().get('title') == route_title:
                route_id = route.id
                route = RouteCreateSchema(**route.to_dict())
                return route, route_id
        return None
