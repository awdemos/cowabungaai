"""Tests for backend constants."""

from cowabunga_api.backend.constants import (
    THIRTY_DAYS_SECONDS,
    TOP_K,
    DEFAULT_MAX_COMPLETION_TOKENS,
    DEFAULT_MAX_PROMPT_TOKENS,
)


def test_thirty_days_seconds():
    """THIRTY_DAYS_SECONDS should equal 30 days in seconds."""
    assert THIRTY_DAYS_SECONDS == 60 * 60 * 24 * 30


def test_top_k():
    """TOP_K should be a positive integer."""
    assert TOP_K == 5


def test_default_max_completion_tokens():
    """DEFAULT_MAX_COMPLETION_TOKENS should be 4096."""
    assert DEFAULT_MAX_COMPLETION_TOKENS == 4096


def test_default_max_prompt_tokens():
    """DEFAULT_MAX_PROMPT_TOKENS should be 4096."""
    assert DEFAULT_MAX_PROMPT_TOKENS == 4096
