"""Tests for Turso authentication module."""

import pytest
from datetime import datetime, timedelta
from cowabunga_api.data.database.turso_auth import User, UserResponse, Session


def test_user_creation():
    """Test User dataclass can be created."""
    user = User(id="user-123", email="test@example.com")
    assert user.id == "user-123"
    assert user.email == "test@example.com"
    assert user.metadata == {}
    assert user.is_active is True
    assert user.is_admin is False


def test_user_with_metadata():
    """Test User dataclass with custom metadata."""
    user = User(id="user-123", email="test@example.com", metadata={"role": "admin"})
    assert user.metadata == {"role": "admin"}


def test_user_response():
    """Test UserResponse wrapper."""
    user = User(id="user-123", email="test@example.com")
    response = UserResponse(user=user)
    assert response.user.id == "user-123"


def test_session_creation():
    """Test Session dataclass can be created."""
    expires = datetime.utcnow() + timedelta(hours=24)
    session = Session(
        id="sess-123",
        user_id="user-123",
        token_hash="abc123",
        expires_at=expires,
    )
    assert session.id == "sess-123"
    assert session.user_id == "user-123"
    assert session.token_hash == "abc123"
