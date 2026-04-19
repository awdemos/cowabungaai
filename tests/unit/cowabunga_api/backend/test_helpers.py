"""Tests for backend helper functions."""

import pytest
from cowabunga_api.backend.helpers import grpc_chat_role, object_or_default


def test_grpc_chat_role_user():
    """Test converting user role string."""
    result = grpc_chat_role("user")
    assert result is not None


def test_grpc_chat_role_system():
    """Test converting system role string."""
    result = grpc_chat_role("system")
    assert result is not None


def test_grpc_chat_role_assistant():
    """Test converting assistant role string."""
    result = grpc_chat_role("assistant")
    assert result is not None


def test_grpc_chat_role_function():
    """Test converting function role string."""
    result = grpc_chat_role("function")
    assert result is not None


def test_grpc_chat_role_unknown():
    """Test converting unknown role string returns None."""
    result = grpc_chat_role("unknown_role")
    assert result is None


def test_object_or_default_with_value():
    """Test object_or_default returns object when not None."""
    assert object_or_default("value", "default") == "value"
    assert object_or_default(42, 0) == 42
    assert object_or_default([1, 2], []) == [1, 2]


def test_object_or_default_with_none():
    """Test object_or_default returns default when None."""
    assert object_or_default(None, "default") == "default"
    assert object_or_default(None, 0) == 0
    assert object_or_default(None, []) == []


def test_object_or_default_with_falsy_values():
    """Test object_or_default with falsy but not None values."""
    assert object_or_default(0, 100) == 0
    assert object_or_default("", "default") == ""
    assert object_or_default(False, True) is False
    assert object_or_default([], [1]) == []
