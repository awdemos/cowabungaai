"""Unit tests for TursoClient implementation."""

import httpx
import pytest
import pytest_asyncio

from cowabunga_api.data.database.base import DatabaseClient
from cowabunga_api.data.database.turso_client import TursoClient, TursoQueryBuilder

BASE_URL = "http://turso-test:8080"


class FakeResponse:
    """Minimal stand-in for httpx.Response driven by canned JSON."""

    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


class FakeHTTPClient:
    """Records posted requests and replies from a canned v2 response queue."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.requests: list[dict] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def post(self, url, json=None, headers=None):
        self.requests.append({"url": url, "json": json, "headers": headers})
        assert self._responses, "No canned response left for POST"
        item = self._responses.pop(0)
        if isinstance(item, tuple):
            payload, status = item
            return FakeResponse(payload, status_code=status)
        return FakeResponse(item)


def libsql_response(columns, rows):
    """Build a v2 pipeline response body mapping to one legacy result set."""
    return {
        "results": [
            {
                "type": "ok",
                "response": {
                    "result": {
                        "cols": [{"name": c} for c in columns],
                        "rows": [[{"value": v} for v in row] for row in rows],
                    }
                },
            }
        ]
    }


def v2_sql(request_entry):
    """Extract the SQL text from a v2 pipeline execute request."""
    return request_entry["stmt"]["sql"]


@pytest.fixture
def http_client_factory(monkeypatch):
    """Patch httpx.AsyncClient in turso_client to return queued responses."""
    created = []

    def _install(responses):
        fake = FakeHTTPClient(responses)
        created.append(fake)

        class _Factory:
            def __init__(self, *args, **kwargs):
                pass

            async def __aenter__(self):
                return fake

            async def __aexit__(self, *args):
                return False

        monkeypatch.setattr(
            "cowabunga_api.data.database.turso_client.httpx.AsyncClient", _Factory
        )
        return fake

    return _install


@pytest_asyncio.fixture
async def turso_client(http_client_factory):
    """Create a TursoClient against a mocked, healthy libsql-server."""
    http_client_factory([libsql_response(["1"], [[1]])])
    return await TursoClient.create(base_url=BASE_URL)


@pytest.mark.asyncio
class TestTursoClient:
    """Test TursoClient functionality."""

    async def test_create_client(self, http_client_factory):
        fake = http_client_factory([libsql_response(["1"], [[1]])])
        client = await TursoClient.create(base_url=BASE_URL)

        assert client is not None
        assert isinstance(client, DatabaseClient)
        assert client.base_url == BASE_URL
        # create() must hit the v2 pipeline endpoint with a health-check
        assert fake.requests[0]["url"] == f"{BASE_URL}/v2/pipeline"
        requests = fake.requests[0]["json"]["requests"]
        assert requests[0]["type"] == "execute"
        assert v2_sql(requests[0]) == "SELECT 1"
        assert requests[-1] == {"type": "close"}

    async def test_create_client_unhealthy(self, http_client_factory):
        http_client_factory([([], 503)])

        with pytest.raises(ConnectionError):
            await TursoClient.create(base_url=BASE_URL)

    async def test_table_returns_query_builder(self, turso_client):
        """Test that table() returns QueryBuilder."""
        builder = turso_client.table("test_users")
        assert isinstance(builder, TursoQueryBuilder)
        assert builder.table_name == "test_users"

    async def test_auth_client_exists(self, turso_client):
        """Test that auth client is available."""
        assert turso_client.auth is not None

    async def test_options_exists(self, turso_client):
        """Test that options object exists."""
        assert turso_client.options is not None
        assert hasattr(turso_client.options, "headers")


@pytest.mark.asyncio
class TestTursoQueryBuilder:
    """Test TursoQueryBuilder functionality."""

    async def test_insert(self, turso_client, http_client_factory):
        http_client_factory(
            [libsql_response(["id", "email"], [["1", "test@example.com"]])]
        )

        result = await (
            turso_client.table("test_users")
            .insert({"id": "1", "email": "test@example.com", "name": "Test User"})
            .execute()
        )

        assert result.error is None
        assert len(result.data) == 1
        assert result.data[0]["email"] == "test@example.com"

    async def test_select(self, turso_client, http_client_factory):
        fake = http_client_factory(
            [libsql_response(["id", "email"], [["1", "test@example.com"]])]
        )

        result = await turso_client.table("test_users").select("*").execute()

        assert result.error is None
        assert len(result.data) == 1
        request = fake.requests[0]["json"]["requests"][0]
        assert v2_sql(request) == "SELECT * FROM test_users"

    async def test_select_with_filter(self, turso_client, http_client_factory):
        fake = http_client_factory([libsql_response(["id", "email"], [["1", "u1"]])])

        result = await (
            turso_client.table("test_users").select("*").eq("id", "1").execute()
        )

        assert result.error is None
        assert len(result.data) == 1
        request = fake.requests[0]["json"]["requests"][0]
        assert v2_sql(request) == "SELECT * FROM test_users WHERE id = ?"
        assert request["stmt"]["args"] == [{"type": "text", "value": "1"}]

    async def test_update(self, turso_client, http_client_factory):
        # _execute_update runs the UPDATE then re-SELECTs the filtered rows
        http_client_factory(
            [
                libsql_response([], []),
                libsql_response(["id", "name"], [["1", "New Name"]]),
            ]
        )

        update_result = await (
            turso_client.table("test_users")
            .update({"name": "New Name"})
            .eq("id", "1")
            .execute()
        )

        assert update_result.error is None
        assert update_result.data[0]["name"] == "New Name"

    async def test_delete(self, turso_client, http_client_factory):
        # _execute_delete runs SELECT-then-DELETE against the same filters
        http_client_factory(
            [
                libsql_response(["id"], [["1"]]),
                libsql_response([], []),
            ]
        )

        delete_result = await (
            turso_client.table("test_users").delete().eq("id", "1").execute()
        )

        assert delete_result.error is None

    async def test_error_response(self, turso_client, http_client_factory):
        http_client_factory(
            [{"results": [{"type": "error", "error": {"message": "no such table"}}]}]
        )

        result = await turso_client.table("missing").select("*").execute()

        assert result.data == []
        assert "no such table" in result.error

    async def test_auth_header_sent(self, http_client_factory):
        http_client_factory([libsql_response(["1"], [[1]])])
        client = await TursoClient.create(base_url=BASE_URL, auth_token="secret")

        fake = http_client_factory([libsql_response(["id"], [["1"]])])
        await client.table("test_users").select("*").execute()

        headers = fake.requests[0]["headers"]
        assert headers["Authorization"] == "Bearer secret"


@pytest.mark.asyncio
class TestTursoAuthClient:
    """Test TursoAuthClient functionality."""

    async def test_get_user_without_token_raises(self, turso_client):
        """get_user with no token and no session must fail."""
        with pytest.raises(Exception):
            await turso_client.auth.get_user()

    async def test_get_user_with_api_key_token(self, turso_client):
        """API-key-shaped tokens resolve to the api-key user."""
        user = await turso_client.auth.get_user("lfai_" + "a" * 64 + "_checksum")

        assert user is not None
        assert user.user.id == "api-key-user"

    async def test_get_user_with_jwt_token(self, turso_client):
        """JWT-shaped tokens resolve to the jwt user."""
        user = await turso_client.auth.get_user("header.payload.signature")

        assert user is not None
        assert user.user.id == "jwt-user"

    async def test_set_session_stores_token(self, turso_client):
        await turso_client.auth.set_session("access-token", "refresh-token")
        assert turso_client.auth._access_token == "access-token"
