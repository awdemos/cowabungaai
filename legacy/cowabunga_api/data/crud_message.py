"""CRUD Operations for Message."""

from openai.types.beta.threads import Message
from cowabunga_api.data.crud_base import CRUDBase
from cowabunga_api.data.database.base import DatabaseClient


class CRUDMessage(CRUDBase[Message]):
    """CRUD Operations for message"""

    def __init__(self, db: DatabaseClient):
        super().__init__(db=db, model=Message, table_name="message_objects")

    async def create(self, object_: Message) -> Message | None:
        if object_.metadata is None:
            object_.metadata = {}

        return await super().create(object_)
