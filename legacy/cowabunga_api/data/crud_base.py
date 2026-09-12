"""Generic CRUD operations for pydantic models backed by a DatabaseClient."""

import os

from typing import Generic, TypeVar
from pydantic import BaseModel

from cowabunga_api.data.database.base import DatabaseClient

ModelType = TypeVar("ModelType", bound=BaseModel)



def _row_to_model_kwargs(model: type[ModelType], row: dict) -> dict:
    """Coerce a raw DB row into model kwargs.

    libsql returns dict/list columns as JSON text and omit-type columns as
    NULL; align them with the model so validation passes.
    """
    fields = model.model_fields
    kwargs = {}
    for key, value in row.items():
        if key not in fields:
            continue
        field_info = fields[key]
        ann = field_info.annotation
        is_text = isinstance(value, str)
        if is_text:
            import json as _json
            def looks_json(s):
                s2 = s.strip()
                return s2[:1] in "[{" and s2[-1:] in "]}"
            origin = getattr(ann, "__origin__", None)
            from typing import Union, get_args
            target = ann
            if origin is Union:
                args = [a for a in get_args(ann) if a not in (type(None),)]
                if len(args) == 1:
                    target = args[0]
            t_origin = getattr(target, "__origin__", None)
            # Python-repr strings (e.g. "[{'text': ...}]" or "{'user_id': ...}")
            # written by dict[str, Any]-style writers — parse via ast before json
            s3 = value.strip()
            if t_origin in (list, dict) and s3[:1] in "[{" and not looks_json(s3):
                import ast as _ast
                try:
                    parsed = _ast.literal_eval(s3)
                    if isinstance(parsed, (list, dict)):
                        value = parsed
                except Exception:
                    pass
            if looks_json(value) and (t_origin in (list, dict) or target in (list, dict)):
                parsed = None
                try:
                    parsed = _json.loads(value)
                except Exception:
                    pass
                if parsed is None and isinstance(value, str):
                    # repr-string written with single quotes ("[{'text': ...}]")
                    import ast as _ast
                    try:
                        parsed = _ast.literal_eval(value)
                    except Exception:
                        parsed = None
                if isinstance(parsed, (list, dict)):
                    value = parsed
            # timestamps come back as TEXT/NULL — numeric strings cast to int
            if is_text and isinstance(value, str) and value.strip().isdigit() and target in (int, float):
                value = int(value) if target is int else float(value)
        kwargs[key] = value
    # Schema drift: the built message_objects table has no `status` column
    # (openai(Message) requires it) — fill a valid default so rows cast.
    fields = model.model_fields  # noqa: F841 (re-bind for clarity)
    if "status" in fields and "status" not in kwargs:
        kwargs["status"] = "completed"
    return kwargs

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

        try:
            # Tolerate schema/model drift: ask the DB for this table's
            # real columns and filter the model dump down to them.
            if hasattr(self.db, "table_columns"):
                existing = set(await self.db.table_columns(self.table_name))
            else:
                existing = set()
            if existing:
                dict_ = {k: v for k, v in dict_.items() if k in existing}
        except Exception:
            pass

        if "id" in dict_ and not dict_.get(
            "id"
        ):  # There are cases where the id is provided
            del dict_["id"]
        # libsql rebuilds of the pg schema may lack uuid defaults on some
        # tables (assistant_objects) — generate a client-side identifier
        # whenever the insert has no id and the model expects one.
        if "id" in object_.model_fields and not any(k == "id" for k in dict_):
            dict_["id"] = os.urandom(16).hex()
        # Only delete created_at if it is <= 0, the db time is not adequate for message ordering
        if "created_at" in dict_ and not (
            isinstance(dict_["created_at"], int) and dict_["created_at"] > 0
        ):
            del dict_["created_at"]

        result = await self.db.table(self.table_name).insert(dict_).execute()

        response = result.data
        if response and len(response) > 0:
            row = response[0]
            row.pop("user_id", None)
            # sqlite/libsql round-trips some values as text (lists/dicts) and
            # leaves app-owned fields NULL — rebuild the model from the
            # validated input object and overlay only db-generated fields.
            merged = {**_row_to_model_kwargs(self.model, row)}
            base = object_.model_dump()
            for k, v in base.items():
                merged.setdefault(k, v)
            try:
                return self.model(**merged)
            except Exception:
                # Fall back to input shape with db-generated id/created_at
                fallback = object_.model_dump()
                fallback["id"] = row.get("id") or fallback.get("id")
                fallback["created_at"] = row.get("created_at") or fallback.get("created_at")
                return self.model(**fallback)
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
                try:
                    return self.model(**_row_to_model_kwargs(self.model, response[0]))
                except Exception:
                    return None
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
        out = []
        for item in response:
            try:
                out.append(self.model(**_row_to_model_kwargs(self.model, item)))
            except Exception as exc:
                # Skip uncastable rows rather than failing the whole page
                import sys as _sys
                print(f"[crud-list] skipped {self.table_name} row {item.get('id')}: {exc}", file=_sys.stderr)
                continue
        return out

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
                try:
                    return self.model(**_row_to_model_kwargs(self.model, response[0]))
                except Exception:
                    return None
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

        return bool(getattr(result, "data", None))

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
