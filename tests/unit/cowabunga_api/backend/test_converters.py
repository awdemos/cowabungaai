"""Tests for backend converters."""

import pytest
from cowabunga_api.backend.converters import from_content_param_to_content


def test_from_content_param_to_content_string():
    """Test converting a string to MessageContent."""
    result = from_content_param_to_content("hello world")
    assert result.type == "text"
    assert result.text.value == "hello world"


def test_from_content_param_to_content_empty_string():
    """Test converting an empty string to MessageContent."""
    result = from_content_param_to_content("")
    assert result.type == "text"
    assert result.text.value == ""


def test_from_content_param_to_content_parts():
    """Test converting MessageContentPartParam iterable to MessageContent."""
    parts = [{"text": "hello "}, {"text": "world"}]
    result = from_content_param_to_content(parts)
    assert result.type == "text"
    assert result.text.value == "hello world"


def test_from_content_param_to_content_empty_parts():
    """Test converting empty parts list to MessageContent."""
    result = from_content_param_to_content([])
    assert result.type == "text"
    assert result.text.value == ""
