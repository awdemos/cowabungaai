"""CRUD Operations for VectorStore."""

from typing import Generic, TypeVar
from pydantic import BaseModel

from cowabunga_api.data.database.base import DatabaseClient

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    """CRUD Operations"""

    def __init__(self, db: DatabaseClient, model: type[ModelType], table_name: str):
        self.model = model
        self.table_name = table_name
        self.db = db

    async def create(self, object_: ModelType) -> ModelType | None:
        """Create new row."""

        dict_ = object_.model_dump()
        current_user = await self.get_current_user()
        dict_["user_id"] = current_user["user_id"]

        if "id" in dict_ and not dict_.get(
            "id"
        ):  # There are cases where the id is provided
            del dict_["id"]
        # Only delete created_at if it is <= 0, the db time is not adequate for message ordering
        if "created_at" in dict_ and not (
            isinstance(dict_["created_at"], int) and dict_["created_at"] > 0
        ):
            del dict_["created_at"]

        result = await self.db.table(self.table_name).insert(dict_).execute()

        response = result.data
        if response and len(response) > 0:
            if "user_id" in response[0]:
                del response[0]["user_id"]
            return self.model(**response[0])
        return None

    async def get(self, filters: dict | None = None) -> ModelType | None:
        """Get row by filters."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        current_user = await self.get_current_user()
        if not current_user["is_admin"]:
            query = query.eq("user_id", current_user["user_id"])

        result = await query.execute()

        try:
            response = result.data
            if response and len(response) > 0:
                if "user_id" in response[0]:
                    del response[0]["user_id"]
                return self.model(**response[0])
            return None
        except (IndexError, AttributeError):
            return None

    async def list(self, filters: dict | None = None) -> list[ModelType]:
        """List all rows."""
        query = self.db.table(self.table_name).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        current_user = await self.get_current_user()
        if not current_user["is_admin"]:
            query = query.eq("user_id", current_user["user_id"])

        result = await query.execute()

        response = result.data if hasattr(result, 'data') and result.data else []
        for item in response:
            if "user_id" in item:
                del item["user_id"]
        return [self.model(**item) for item in response]

    async def update(self, id_: str, object_: ModelType) -> ModelType | None:
        """Update a row by its ID."""

        dict_ = object_.model_dump()
        # Do NOT modify user_id in the update dict

        current_user = await self.get_current_user()
        query = self.db.table(self.table_name).update(dict_).eq("id", id_)
        if not current_user["is_admin"]:
            query = query.eq("user_id", current_user["user_id"])

        result = await query.execute()

        try:
            response = result.data
            if response and len(response) > 0:
                if "user_id" in response[0]:
                    del response[0]["user_id"]
                return self.model(**response[0])
            return None
        except (IndexError, AttributeError):
            return None

    async def delete(self, filters: dict | None = None) -> bool:
        """Delete a row by filters."""
        query = self.db.table(self.table_name).delete()

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        current_user = await self.get_current_user()
        if not current_user["is_admin"]:
            query = query.eq("user_id", current_user["user_id"])

        result = await query.execute()

        return bool(result.data) if hasattr(result, 'data') else False

    async def get_current_user(self) -> dict:
        """Get the current user with admin status."""
        return await get_current_user(self.db)

    async def _get_user_id(self) -> str:
        """Get the user_id from the API key."""

        user = await self.get_current_user()
        return user["user_id"]


async def get_user_id(db: DatabaseClient) -> str:
    """Get the user_id from the API key."""

    if db.options.headers.get("x-custom-api-key"):
        result = await db.table("api_keys").select("user_id").execute()
        if result.data and len(result.data) > 0:
            user_id: str = result.data[0]["user_id"]
        else:
            user_id = "anonymous"
    else:
        try:
            user = await db.auth.get_user()
            user_id = user.user.id if hasattr(user, 'user') else str(user)
        except Exception:
            user_id = "anonymous"

    return user_id


async def get_current_user(db: DatabaseClient) -> dict:
    """Get the current user with admin status."""

    user_id = await get_user_id(db)

    if not user_id or user_id == "anonymous":
        raise Exception("No authenticated user")

    result = await db.table("users").select("is_admin").eq("id", user_id).execute()
    is_admin = False
    if result.data and len(result.data) > 0:
        is_admin = result.data[0].get("is_admin", False)

    return {"user_id": user_id, "is_admin": is_admin}
