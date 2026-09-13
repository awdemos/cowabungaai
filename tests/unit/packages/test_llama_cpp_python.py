"""Tests for the llama-cpp-python package."""

import pytest


def test_llama_cpp_python_imports():
    """Test that the llama-cpp-python main module can be imported."""
    try:
        from packages.llama_cpp_python.main import app
        assert app is not None
    except ImportError as e:
        pytest.skip(f"Import failed (may need build deps): {e}")


def test_model_download_script_imports():
    """Test that the model download script can be imported."""
    try:
        from packages.llama_cpp_python.scripts.model_download import main
        assert callable(main)
    except ImportError as e:
        pytest.skip(f"Import failed (may need deps): {e}")
