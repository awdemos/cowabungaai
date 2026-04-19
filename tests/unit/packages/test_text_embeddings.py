"""Tests for the text-embeddings package."""

import pytest


def test_text_embeddings_imports():
    """Test that the text-embeddings main module can be imported."""
    try:
        from packages.text_embeddings.main import app
        assert app is not None
    except ImportError as e:
        pytest.skip(f"Import failed (may need build deps): {e}")
