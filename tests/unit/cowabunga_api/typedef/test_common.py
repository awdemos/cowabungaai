"""Tests for common typedef modules."""

from cowabunga_api.typedef.common import Usage


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
