"""Direct import tests for untested modules."""


def test_import_cowabunga_evals_runners_niah_runner():
    from cowabunga_evals.runners import niah_runner
    assert niah_runner is not None


def test_import_cowabunga_evals_runners_qa_runner():
    from cowabunga_evals.runners import qa_runner
    assert qa_runner is not None


def test_import_cowabunga_api_backend_composer():
    from cowabunga_api.backend import composer
    assert composer is not None


def test_import_cowabunga_api_backend_grpc_client():
    from cowabunga_api.backend import grpc_client
    assert grpc_client is not None


def test_import_cowabunga_api_backend_rag_query():
    from cowabunga_api.backend.rag import query
    assert query is not None


def test_import_cowabunga_api_data_database_turso_auth():
    from cowabunga_api.data.database import turso_auth
    assert turso_auth is not None


def test_import_cowabunga_sdk_serve():
    from cowabunga_sdk import serve
    assert serve is not None


def test_import_cowabunga_api_routers_openai_chat():
    from cowabunga_api.routers.openai import chat
    assert chat is not None
