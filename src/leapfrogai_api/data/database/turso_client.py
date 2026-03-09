"""Turso database client implementing DatabaseClient interface.

HTTP client for official libsql-server (ghcr.io/tursodatabase/libsql-server).
API: POST / with {"statements":[{"query":"SQL","params":[...]}]}
Response: [{"results":{"columns":[...],"rows":[[...]]}}]
"""

from typing import Any, Optional
from dataclasses import dataclass

import httpx

from leapfrogai_api.data.database.base import DatabaseClient, QueryBuilder, AuthClient  # type: ignore


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
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            statements.append({"query": sql, "params": list(record.values())})

        payload = {"statements": statements}
        response = await client.post(f"{self.base_url}/", json=payload, headers=headers)
        response.raise_for_status()

        # For INSERT, return the inserted data (no RETURNING in base SQLite)
        return TursoResult(data=records)

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

        if self._current_user_id:
            return UserResponse(user=User(id=self._current_user_id))

        if token and token.startswith("lfai_"):
            return UserResponse(user=User(id="api-key-user"))

        raise Exception("No authenticated user")

    async def set_session(self, access_token: str, refresh_token: str) -> None:
        self._access_token = access_token


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

    @property
    def auth(self) -> TursoAuthClient:
        return self._auth

    @property
    def options(self) -> TursoOptions:
        return self._options

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # libsql-server doesn't have /health, use SELECT 1
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
