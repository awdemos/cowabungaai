"""Tests for the CowabungaAI evaluations main module."""

import pytest
from cowabunga_evals.main import RAGEvaluator, ALL_EVALS


def test_rag_evaluator_default_init():
    """Test RAGEvaluator initializes with None eval_list."""
    evaluator = RAGEvaluator()
    assert evaluator.eval_list is None
    assert evaluator.eval_results == {}


def test_set_evaluations_default():
    """Test setting evaluations to default (all)."""
    evaluator = RAGEvaluator()
    evaluator.set_evaluations()
    assert evaluator.eval_list == ALL_EVALS


def test_set_evaluations_subset():
    """Test setting evaluations to a subset."""
    evaluator = RAGEvaluator()
    evaluator.set_evaluations(["niah_eval", "qa_eval"])
    assert evaluator.eval_list == ["niah_eval", "qa_eval"]


def test_set_evaluations_invalid():
    """Test that invalid evaluation names raise AttributeError."""
    evaluator = RAGEvaluator()
    with pytest.raises(AttributeError) as exc_info:
        evaluator.set_evaluations(["invalid_eval"])
    assert "invalid_eval" in str(exc_info.value)
    assert "not an available evaluation" in str(exc_info.value)


def test_run_evals_without_setting():
    """Test that running evals without setting them raises AttributeError."""
    evaluator = RAGEvaluator()
    with pytest.raises(AttributeError) as exc_info:
        evaluator.run_evals()
    assert "has not been set" in str(exc_info.value)
