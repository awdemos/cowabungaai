"""Tests for SDK utils module."""

import pytest
from cowabunga_sdk.utils import import_app


def test_import_app_with_colon():
    """Test import_app with module:attribute format."""
    app = import_app("cowabunga_sdk.utils:import_app")
    assert callable(app)


def test_import_app_without_colon():
    """Test import_app without colon defaults to 'application'."""
    with pytest.raises(Exception):
        import_app("cowabunga_sdk.utils")


def test_import_app_missing_module():
    """Test import_app with nonexistent module."""
    with pytest.raises(ImportError):
        import_app("nonexistent_module:app")


def test_import_app_invalid_syntax():
    """Test import_app with invalid attribute syntax."""
    with pytest.raises(Exception):
        import_app("cowabunga_sdk.utils:invalid[syntax")
