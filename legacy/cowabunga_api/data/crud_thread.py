"""CRUD Operations for Thread."""

from openai.types.beta import Thread
from cowabunga_api.data.crud_base import CRUDBase
from cowabunga_api.data.database.base import DatabaseClient


class CRUDThread(CRUDBase[Thread]):
    """CRUD Operations for thread"""

    def __init__(self, db: DatabaseClient):
        super().__init__(db=db, model=Thread, table_name="thread_objects")
