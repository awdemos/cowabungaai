"""Smoke tests — verify untested modules can be imported without errors.

These tests provide baseline coverage for modules that lack dedicated tests.
Import failures usually indicate broken dependencies or circular imports.
"""

import pytest


# src/cowabunga_api backend modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_api.backend.composer",
        "cowabunga_api.backend.converters",
        "cowabunga_api.backend.grpc_client",
        "cowabunga_api.backend.helpers",
        "cowabunga_api.backend.rag.leapfrogai_embeddings",
        "cowabunga_api.backend.rag.query",
    ],
)
def test_backend_module_imports(module):
    """Test that backend modules can be imported."""
    __import__(module)


# src/cowabunga_api data modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_api.data.crud_assistant",
        "cowabunga_api.data.crud_file_object",
        "cowabunga_api.data.crud_run",
        "cowabunga_api.data.crud_vector_content",
        "cowabunga_api.data.database.supabase_client",
        "cowabunga_api.data.database.turso_auth",
    ],
)
def test_data_module_imports(module):
    """Test that data modules can be imported."""
    __import__(module)


# src/cowabunga_api router modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_api.routers.cowabunga.models",
        "cowabunga_api.routers.cowabunga.rag",
        "cowabunga_api.routers.openai.audio",
        "cowabunga_api.routers.openai.chat",
        "cowabunga_api.routers.openai.runs_steps",
    ],
)
def test_router_module_imports(module):
    """Test that router modules can be imported."""
    __import__(module)


# src/cowabunga_api typedef modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_api.typedef.audio.audio_types",
        "cowabunga_api.typedef.common",
        "cowabunga_api.typedef.models.model_types",
        "cowabunga_api.typedef.rag.rag_types",
    ],
)
def test_typedef_module_imports(module):
    """Test that typedef modules can be imported."""
    __import__(module)


# src/cowabunga_evals modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_evals.evals.human_eval",
        "cowabunga_evals.evals.mmlu",
        "cowabunga_evals.evals.niah_eval",
        "cowabunga_evals.evals.qa_eval",
        "cowabunga_evals.main",
        "cowabunga_evals.metrics.annotation_relevancy",
        "cowabunga_evals.metrics.correctness",
        "cowabunga_evals.metrics.niah_metrics",
        "cowabunga_evals.models.claude_sonnet",
        "cowabunga_evals.models.lfai",
        "cowabunga_evals.runners.niah_runner",
        "cowabunga_evals.runners.qa_runner",
    ],
)
def test_evals_module_imports(module):
    """Test that evals modules can be imported."""
    __import__(module)


# src/cowabunga_sdk modules
@pytest.mark.parametrize(
    "module",
    [
        "cowabunga_sdk.llm",
        "cowabunga_sdk.serve",
        "cowabunga_sdk.utils",
    ],
)
def test_sdk_module_imports(module):
    """Test that SDK modules can be imported."""
    __import__(module)
