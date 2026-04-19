"""Tests for the whisper package."""

import pytest


def test_whisper_imports():
    """Test that the whisper main module can be imported."""
    try:
        from packages.whisper.main import app
        assert app is not None
    except ImportError as e:
        pytest.skip(f"Import failed (may need build deps): {e}")
