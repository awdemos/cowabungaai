"""Tests for eval defaults module."""

from cowabunga_evals.utils.defaults import DEFAULT_INSTRUCTION_TEMPLATE


def test_default_instruction_template_is_string():
    """DEFAULT_INSTRUCTION_TEMPLATE should be a non-empty string."""
    assert isinstance(DEFAULT_INSTRUCTION_TEMPLATE, str)
    assert len(DEFAULT_INSTRUCTION_TEMPLATE) > 0
