from typing import Optional

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from envs import Env


class FirebaseDB:
    def __init__(self):
        self.db: Optional = None

    def init_db(self):
        cred = credentials.Certificate(Env.db.CREDENTIAL_JSON)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()


db = FirebaseDB()
