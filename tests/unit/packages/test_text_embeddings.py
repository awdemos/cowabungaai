"""Tests for the text-embeddings package."""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_module(name: str, path: Path):
    """Load a module from a file path (handles hyphenated package dirs)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"cannot load {name} from {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_text_embeddings_imports():
    """Test that the text-embeddings main module exposes a backend class."""
    pytest.importorskip("cowabunga_sdk")
    pytest.importorskip("InstructorEmbedding")
    main = _load_module(
        "text_embeddings_main", REPO_ROOT / "packages/text-embeddings/main.py"
    )
    assert hasattr(main, "InstructorEmbedding")
