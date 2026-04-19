"""Tests for backend helper functions."""

import pytest
from cowabunga_api.backend.helpers import grpc_chat_role


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



