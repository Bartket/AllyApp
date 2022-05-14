import uuid

from config.db import db
from .schemas import LocationCreateSchema


class Locations:

    @staticmethod
    def create_document(location: LocationCreateSchema):
        document = db.db.collection('locations').document(str(uuid.uuid4()))
        document.set(location.dict())
