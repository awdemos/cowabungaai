"""Tests for SDK errors module."""

import pytest
from cowabunga_sdk.errors import AppImportError


def test_app_import_error_is_exception():
    """AppImportError should be a subclass of Exception."""
    assert issubclass(AppImportError, Exception)


def test_app_import_error_can_be_raised():
    """AppImportError can be raised and caught."""
    with pytest.raises(AppImportError):
        raise AppImportError("import failed")
