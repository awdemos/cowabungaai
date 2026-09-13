"""Tests for common typedef modules."""

import pytest
from cowabunga_api.typedef.common import MetadataObject, Usage


def test_metadata_object_creation():
    """Test MetadataObject can be created with arbitrary attributes."""
    obj = MetadataObject(name="test", value=42)
    assert obj.name == "test"
    assert obj.value == 42


def test_metadata_object_missing_attribute():
    """Test MetadataObject returns None for missing attributes."""
    obj = MetadataObject()
    assert obj.nonexistent is None


def test_usage_creation():
    """Test Usage model can be instantiated."""
    usage = Usage(prompt_tokens=10, total_tokens=25)
    assert usage.prompt_tokens == 10
    assert usage.total_tokens == 25
    assert usage.completion_tokens is not None


def test_usage_with_completion_tokens():
    """Test Usage model with explicit completion_tokens."""
    usage = Usage(prompt_tokens=10, completion_tokens=15, total_tokens=25)
    assert usage.completion_tokens == 15
