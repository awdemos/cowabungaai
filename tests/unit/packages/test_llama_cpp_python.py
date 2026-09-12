"""Tests for the llama-cpp-python package."""

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


def test_llama_cpp_python_imports():
    """Test that the llama-cpp-python main module exposes a Model backend."""
    pytest.importorskip("llama_cpp_python")
    pytest.importorskip("cowabunga_sdk")
    main = _load_module(
        "llama_cpp_python_main", REPO_ROOT / "packages/llama-cpp-python/main.py"
    )
    assert hasattr(main, "Model")


def test_model_download_script_imports():
    """Test that the model download script can be imported."""
    module = _load_module(
        "llama_cpp_python_model_download",
        REPO_ROOT / "packages/llama-cpp-python/scripts/model_download.py",
    )
    assert callable(module.download_model)
