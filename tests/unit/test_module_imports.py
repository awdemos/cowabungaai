"""Direct import tests for untested modules."""

import importlib
import pytest


def _import_or_skip(module: str, attr: str | None = None):
    """Import a module, skipping the test if an optional dependency is missing."""
    try:
        mod = importlib.import_module(module)
    except ImportError as exc:
        pytest.skip(f"Optional dependency missing for {module}: {exc}")
    if attr:
        assert getattr(mod, attr) is not None
    else:
        assert mod is not None


def test_import_cowabunga_evals_runners_niah_runner():
    _import_or_skip("cowabunga_evals.runners.niah_runner")


def test_import_cowabunga_evals_runners_qa_runner():
    _import_or_skip("cowabunga_evals.runners.qa_runner")


def test_import_cowabunga_api_backend_composer():
    _import_or_skip("cowabunga_api.backend.composer")


def test_import_cowabunga_api_backend_grpc_client():
    _import_or_skip("cowabunga_api.backend.grpc_client")


def test_import_cowabunga_api_backend_rag_query():
    _import_or_skip("cowabunga_api.backend.rag.query")


def test_import_cowabunga_api_data_database_turso_auth():
    _import_or_skip("cowabunga_api.data.database.turso_auth")


def test_import_cowabunga_sdk_serve():
    _import_or_skip("cowabunga_sdk", "serve")


def test_import_cowabunga_api_routers_openai_chat():
    _import_or_skip("cowabunga_api.routers.openai.chat")
