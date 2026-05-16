"""CRUD Operations for VectorStore."""

import struct
from cowabunga_api.data.crud_base import get_user_id
from cowabunga_api.typedef.vectorstores import SearchItem, SearchResponse
from cowabunga_api.backend.constants import TOP_K
from cowabunga_api.typedef.vectorstores import Vector
from cowabunga_api.data.database.base import DatabaseClient


class CRUDVectorContent:
    """CRUD Operations for VectorStore"""

    def __init__(self, db: DatabaseClient):
        self.db = db
        self.table_name = "vector_content"

    @staticmethod
    def _serialize_embedding(embedding: list[float]) -> bytes:
        """Pack a list of floats into a compact binary F32_BLOB."""
        return struct.pack(f"<{len(embedding)}f", *embedding)

    @staticmethod
    def _deserialize_embedding(data: bytes | str | list) -> list[float]:
        """Unpack binary F32_BLOB or legacy string/list into list of floats."""
        if isinstance(data, bytes):
            count = len(data) // 4
            return list(struct.unpack(f"<{count}f", data))
        if isinstance(data, str):
            import ast
            parsed = ast.literal_eval(data.strip())
            return [float(x) for x in parsed]
        if isinstance(data, list):
            return [float(x) for x in data]
        raise ValueError(f"Unsupported embedding type: {type(data)}")

    async def add_vectors(self, object_: list[Vector]) -> list[Vector]:
        """Create new row."""

        user_id = await get_user_id(self.db)

        rows = []

        for vector in object_:
            dict_ = vector.model_dump()
            dict_["user_id"] = user_id
            if "id" in dict_:
                del dict_["id"]
            dict_["embedding"] = self._serialize_embedding(dict_["embedding"])

            rows.append(dict_)

        result = await self.db.table(self.table_name).insert(rows).execute()

        response = result.data if hasattr(result, "data") else result

        final_response = []
        for item in response:
            if "user_id" in item:
                del item["user_id"]
            item["embedding"] = self._deserialize_embedding(item["embedding"])
            final_response.append(
                Vector(
                    id=item["id"],
                    vector_store_id=item["vector_store_id"],
                    file_id=item["file_id"],
                    content=item["content"],
                    metadata=item["metadata"],
                    embedding=item["embedding"],
                )
            )

        return final_response

    async def get_vector(self, vector_id: str) -> Vector:
        """Get a vector by its ID."""
        result = await self.db.table(self.table_name).select("*").eq("id", vector_id).execute()

        response = result.data

        if response and len(response) > 0:
            item = response[0]
            item["embedding"] = self._deserialize_embedding(item["embedding"])

            return Vector(
                id=item["id"],
                vector_store_id=item["vector_store_id"],
                file_id=item["file_id"],
                content=item["content"],
                metadata=item["metadata"],
                embedding=item["embedding"],
            )
        raise ValueError(f"Vector {vector_id} not found")

    async def delete_vectors(self, vector_store_id: str, file_id: str) -> bool:
        """Delete a vector store file by its ID."""
        result = await self.db.table(self.table_name).delete().eq("vector_store_id", vector_store_id).eq("file_id", file_id).execute()

        response = result.data if hasattr(result, "data") else result

        return bool(response)

    async def similarity_search(
        self, query: list[float], vector_store_id: str, k: int = TOP_K
    ) -> SearchResponse:
        user_id = await get_user_id(self.db)

        params = {
            "query_embedding": query,
            "match_limit": k,
            "vs_id": vector_store_id,
            "user_id": user_id,
        }

        result = await self.db.rpc("match_vectors", params).execute()

        response = result.data if hasattr(result, "data") else result
        return SearchResponse(data=[SearchItem(**item) for item in response])

    @staticmethod
    def string_to_float_list(s: str) -> list[float]:
        import ast
        try:
            cleaned_string = s.strip()
            python_list = ast.literal_eval(cleaned_string)
            return [float(x) for x in python_list]
        except (ValueError, SyntaxError) as e:
            raise e
