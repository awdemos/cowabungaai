"""CRUD Operations for Run."""

from openai.types.beta.threads import Run
from cowabunga_api.data.crud_base import CRUDBase
from cowabunga_api.data.database.base import DatabaseClient


class CRUDRun(CRUDBase[Run]):
    """CRUD Operations for run"""

    def __init__(self, db: DatabaseClient):
        super().__init__(db=db, model=Run, table_name="run_objects")

    async def update(self, id_: str, object_: Run) -> Run | None:
        """Update a run by its ID."""

        dict_ = object_.model_dump()

        result = await self.db.table(self.table_name).update(dict_).eq("id", id_).execute()

        response = result.data

        if response:
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        return None
