"""Turso database client implementing DatabaseClient interface.

HTTP client for official libsql-server (ghcr.io/tursodatabase/libsql-server).
API: POST / with {"statements":[{"query":"SQL","params":[...]}]}
Response: [{"results":{"columns":[...],"rows":[[...]]}}]
"""

from typing import Any, Optional
from dataclasses import dataclass

import httpx

from cowabunga_api.data.database.base import DatabaseClient, QueryBuilder, AuthClient  # type: ignore


@dataclass
class TursoResult:
    data: list[dict]
    error: Optional[str] = None


class TursoQueryBuilder(QueryBuilder):
    def __init__(
        self, base_url: str, table_name: str, auth_token: Optional[str] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.table_name = table_name
        self.auth_token = auth_token
        self._columns = "*"
        self._filters: list[tuple[str, str, Any]] = []
        self._data: Optional[dict | list] = None
        self._operation = "SELECT"
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None

    def select(self, columns: str = "*") -> "TursoQueryBuilder":
        self._columns = columns
        self._operation = "SELECT"
        return self

    def insert(self, data: dict | list) -> "TursoQueryBuilder":
        self._data = data if isinstance(data, list) else [data]
        self._operation = "INSERT"
        return self

    def update(self, data: dict) -> "TursoQueryBuilder":
        self._data = data
        self._operation = "UPDATE"
        return self

    def delete(self) -> "TursoQueryBuilder":
        self._operation = "DELETE"
        return self

    def eq(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, "=", value))
        return self

    def neq(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, "!=", value))
        return self

    def gt(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, ">", value))
        return self

    def gte(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, ">=", value))
        return self

    def lt(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, "<", value))
        return self

    def lte(self, column: str, value: Any) -> "TursoQueryBuilder":
        self._filters.append((column, "<=", value))
        return self

    def order(self, column: str, desc: bool = False) -> "TursoQueryBuilder":
        self._order_by = f"{column} DESC" if desc else column
        return self

    def limit(self, count: int) -> "TursoQueryBuilder":
        self._limit = count
        return self

    def range(self, start: int, end: int) -> "TursoQueryBuilder":
        self._limit = end - start + 1
        self._offset = start
        return self

    def single(self) -> "TursoQueryBuilder":
        self._limit = 1
        return self

    def _build_sql(self) -> tuple[str, list]:
        params = []

        if self._operation == "SELECT":
            sql = f"SELECT {self._columns} FROM {self.table_name}"
        elif self._operation == "DELETE":
            sql = f"DELETE FROM {self.table_name}"
        elif self._operation == "UPDATE":
            assert isinstance(self._data, dict), "UPDATE requires dict data"
            set_clauses = [f"{col} = ?" for col in self._data.keys()]
            sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)}"
            params = list(self._data.values())
        elif self._operation == "INSERT":
            return "", []
        else:
            return "", []

        if self._filters:
            where_clauses = []
            for col, op, val in self._filters:
                where_clauses.append(f"{col} {op} ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(where_clauses)

        if self._order_by:
            sql += f" ORDER BY {self._order_by}"

        if self._limit is not None:
            sql += f" LIMIT {self._limit}"
        if self._offset is not None:
            sql += f" OFFSET {self._offset}"

        return sql, params

    async def _execute_sql(
        self, client: httpx.AsyncClient, sql: str, params: list, headers: dict
    ) -> TursoResult:
        payload = {"statements": [{"query": sql, "params": params}]}
        response = await client.post(f"{self.base_url}/", json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()

        if not results or not isinstance(results, list):
            return TursoResult(data=[])

        first = results[0]
        if "error" in first:
            return TursoResult(data=[], error=first["error"]["message"])

        if "results" not in first:
            return TursoResult(data=[])

        cols = first["results"].get("columns", [])
        rows = first["results"].get("rows", [])
        data = [dict(zip(cols, row)) for row in rows]
        return TursoResult(data=data)

    async def execute(self) -> TursoResult:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"Content-Type": "application/json"}
                if self.auth_token:
                    headers["Authorization"] = f"Bearer {self.auth_token}"

                if self._operation == "INSERT":
                    return await self._execute_insert(client, headers)
                elif self._operation == "UPDATE":
                    return await self._execute_update(client, headers)
                elif self._operation == "DELETE":
                    return await self._execute_delete(client, headers)
                elif self._operation == "SELECT":
                    sql, params = self._build_sql()
                    return await self._execute_sql(client, sql, params, headers)
                else:
                    return TursoResult(data=[], error="Invalid operation")

        except httpx.HTTPError as e:
            return TursoResult(data=[], error=f"HTTP error: {str(e)}")
        except Exception as e:
            return TursoResult(data=[], error=str(e))

    async def _execute_insert(
        self, client: httpx.AsyncClient, headers: dict
    ) -> TursoResult:
        assert self._data is not None, "INSERT requires data"
        records = self._data if isinstance(self._data, list) else [self._data]

        statements = []
        for record in records:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in record])
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
            statements.append({"query": sql, "params": list(record.values())})

        payload = {"statements": statements}
        response = await client.post(f"{self.base_url}/", json=payload, headers=headers)
        response.raise_for_status()

        results = response.json()
        if not results or not isinstance(results, list):
            return TursoResult(data=[])

        all_data = []
        for result in results:
            if "error" in result:
                return TursoResult(data=[], error=result["error"]["message"])
            if "results" in result:
                cols = result["results"].get("columns", [])
                rows = result["results"].get("rows", [])
                for row in rows:
                    all_data.append(dict(zip(cols, row)))

        return TursoResult(data=all_data)

    async def _execute_update(
        self, client: httpx.AsyncClient, headers: dict
    ) -> TursoResult:
        sql, params = self._build_sql()
        await self._execute_sql(client, sql, params, headers)

        # Return updated rows by re-selecting
        self._operation = "SELECT"
        sql, params = self._build_sql()
        return await self._execute_sql(client, sql, params, headers)

    async def _execute_delete(
        self, client: httpx.AsyncClient, headers: dict
    ) -> TursoResult:
        # Get rows before delete
        self._operation = "SELECT"
        sql, params = self._build_sql()
        select_result = await self._execute_sql(client, sql, params, headers)

        # Delete
        self._operation = "DELETE"
        sql, params = self._build_sql()
        await self._execute_sql(client, sql, params, headers)

        return select_result

    async def single(self) -> Optional[dict]:
        result = await self.execute()
        if result.error:
            return None
        return result.data[0] if result.data else None


class TursoAuthClient(AuthClient):
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url
        self._current_user_id = None
        self._access_token = None

    async def get_user(self, token: str | None = None) -> Any:
        from dataclasses import dataclass

        @dataclass
        class UserResponse:
            user: Any

        @dataclass
        class User:
            id: str
            email: str = ""

        # Use stored access token if no token provided
        token = token or self._access_token

        if self._current_user_id:
            return UserResponse(user=User(id=self._current_user_id))

        if token and token.startswith("lfai_"):
            return UserResponse(user=User(id="api-key-user"))

        # Try to extract user_id from JWT-like token
        if token and token.count(".") == 2:
            return UserResponse(user=User(id="jwt-user"))

        raise Exception("No authenticated user")

    async def set_session(self, access_token: str, refresh_token: str) -> None:
        self._access_token = access_token
        # Attempt to extract user_id from JWT
        if access_token and access_token.count(".") == 2:
            try:
                import base64
                import json
                payload_b64 = access_token.split(".")[1]
                # Add padding if needed
                padding = 4 - len(payload_b64) % 4
                if padding != 4:
                    payload_b64 += "=" * padding
                payload = json.loads(base64.urlsafe_b64decode(payload_b64))
                self._current_user_id = payload.get("sub") or payload.get("user_id")
            except Exception:
                pass


class TursoOptions:
    def __init__(self):
        self.headers = {}
        self.auto_refresh_token = False


class TursoClient(DatabaseClient):
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self._auth = TursoAuthClient(base_url)
        self._options = TursoOptions()

    def table(self, table_name: str) -> TursoQueryBuilder:
        return TursoQueryBuilder(self.base_url, table_name, self.auth_token)

    def rpc(self, function_name: str, params: dict | None = None):
        """RPC call wrapper for compatibility.
        
        For Turso, known functions are implemented directly.
        Unknown functions raise NotImplementedError.
        """
        if function_name == "match_vectors":
            # Vector similarity search - will be handled by CRUDVectorContent
            return _MatchVectorsRPC(self, params or {})
        elif function_name == "insert_api_key":
            # API key insertion with generated fields
            return _InsertAPIKeyRPC(self, params or {})
        raise NotImplementedError(f"RPC function '{function_name}' is not implemented for Turso")

    @property
    def auth(self) -> TursoAuthClient:
        return self._auth

    @property
    def options(self) -> TursoOptions:
        return self._options

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                payload = {"statements": [{"query": "SELECT 1", "params": []}]}
                response = await client.post(f"{self.base_url}/", json=payload)
                return response.status_code == 200
        except Exception:
            return False

    @classmethod
    async def create(
        cls,
        base_url: str = "http://turso:8080",
        auth_token: Optional[str] = None,
        **kwargs,
    ) -> "TursoClient":
        client = cls(base_url, auth_token)

        if not await client.health_check():
            raise ConnectionError(f"Cannot connect to Turso service at {base_url}")

        return client


class _MatchVectorsRPC:
    """RPC-compatible wrapper for vector similarity search."""

    def __init__(self, client: TursoClient, params: dict):
        self.client = client
        self.params = params

    async def execute(self) -> TursoResult:
        import struct

        vector_store_id = self.params.get("vs_id")
        query_embedding = self.params.get("query_embedding", [])
        match_limit = self.params.get("match_limit", 10)

        if not vector_store_id or not query_embedding:
            return TursoResult(data=[])

        query_bytes = struct.pack(f"<{len(query_embedding)}f", *query_embedding)

        try:
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                headers = {"Content-Type": "application/json"}
                if self.client.auth_token:
                    headers["Authorization"] = f"Bearer {self.client.auth_token}"

                sql = (
                    "SELECT id, vector_store_id, file_id, content, metadata, "
                    "vector_distance_cos(embedding, vector32(?)) AS similarity "
                    "FROM vector_content WHERE vector_store_id = ? "
                    "AND embedding MATCH vector32(?) "
                    "ORDER BY similarity LIMIT ?"
                )
                payload = {
                    "statements": [
                        {
                            "query": sql,
                            "params": [query_bytes.hex(), vector_store_id, query_bytes.hex(), match_limit],
                        }
                    ]
                }
                response = await http_client.post(
                    f"{self.client.base_url}/", json=payload, headers=headers
                )
                response.raise_for_status()
                results = response.json()

                if not results or not isinstance(results, list):
                    return TursoResult(data=[])

                first = results[0]
                if "error" in first:
                    error_msg = first["error"].get("message", "Unknown error")
                    if (
                        "no such function: vector_distance_cos" in error_msg
                        or "no such index" in error_msg
                    ):
                        return await self._fallback_brute_force(
                            vector_store_id, query_embedding, match_limit
                        )
                    return TursoResult(data=[], error=error_msg)

                if "results" not in first:
                    return TursoResult(data=[])

                cols = first["results"].get("columns", [])
                rows = first["results"].get("rows", [])
                data = [dict(zip(cols, row)) for row in rows]
                return TursoResult(data=data)
        except httpx.HTTPError:
            return await self._fallback_brute_force(
                vector_store_id, query_embedding, match_limit
            )

    async def _fallback_brute_force(
        self, vector_store_id: str, query_embedding: list[float], match_limit: int
    ) -> TursoResult:
        import struct

        result = await self.client.table("vector_content").select("*").eq(
            "vector_store_id", vector_store_id
        ).execute()
        if not result.data:
            return TursoResult(data=[])

        scored = []
        for item in result.data:
            embedding = item.get("embedding")
            if isinstance(embedding, bytes):
                count = len(embedding) // 4
                embedding = list(struct.unpack(f"<{count}f", embedding))
            elif isinstance(embedding, str):
                import ast
                try:
                    embedding = ast.literal_eval(embedding.strip())
                    embedding = [float(x) for x in embedding]
                except (ValueError, SyntaxError):
                    continue
            if embedding and len(embedding) == len(query_embedding):
                score = _cosine_similarity(query_embedding, embedding)
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_k = scored[:match_limit]

        return TursoResult(data=[item for _, item in top_k])


class _InsertAPIKeyRPC:
    """RPC-compatible wrapper for insert_api_key function."""

    def __init__(self, client: TursoClient, params: dict):
        self.client = client
        self.params = params

    async def execute(self) -> TursoResult:
        import time
        import secrets

        data = {
            "id": secrets.token_urlsafe(16),
            "user_id": self.params.get("p_user_id"),
            "api_key": self.params.get("p_api_key"),
            "name": self.params.get("p_name"),
            "created_at": int(time.time()),
            "expires_at": self.params.get("p_expires_at"),
            "checksum": self.params.get("p_checksum"),
            "is_active": True,
        }
        return await self.client.table("api_keys").insert(data).execute()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
