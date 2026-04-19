# __init__.py
# ruff: noqa: F401

try:
    from cowabunga_evals.models.claude_sonnet import ClaudeSonnet
except ImportError:
    ClaudeSonnet = None  # type: ignore[misc,assignment]

from cowabunga_evals.models.lfai import COWABUNGA_Model
