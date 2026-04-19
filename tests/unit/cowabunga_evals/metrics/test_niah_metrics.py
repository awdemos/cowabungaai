"""Tests for NIAH metrics."""

import pytest
from deepeval.test_case import LLMTestCase
from cowabunga_evals.metrics.niah_metrics import NIAH_Retrieval


@pytest.fixture
def niah_metric():
    return NIAH_Retrieval(threshold=1.0)


@pytest.fixture
def successful_test_case():
    return LLMTestCase(
        input="test",
        actual_output="test",
        additional_metadata={"retrieval_score": 1},
    )


@pytest.fixture
def failing_test_case():
    return LLMTestCase(
        input="test",
        actual_output="test",
        additional_metadata={"retrieval_score": 0},
    )


def test_niah_retrieval_success(niah_metric, successful_test_case):
    """Test NIAH retrieval metric with passing score."""
    score = niah_metric.measure(successful_test_case)
    assert score == 1
    assert niah_metric.success is True
    assert "greater than or equal to" in niah_metric.reason


def test_niah_retrieval_failure(niah_metric, failing_test_case):
    """Test NIAH retrieval metric with failing score."""
    score = niah_metric.measure(failing_test_case)
    assert score == 0
    assert niah_metric.success is False
    assert "less than" in niah_metric.reason


def test_niah_retrieval_threshold():
    """Test NIAH retrieval metric respects threshold."""
    metric = NIAH_Retrieval(threshold=0.5)
    test_case = LLMTestCase(
        input="test",
        actual_output="test",
        additional_metadata={"retrieval_score": 0.5},
    )
    score = metric.measure(test_case)
    assert score == 0.5
    assert metric.success is True


@pytest.mark.asyncio
async def test_niah_retrieval_async(niah_metric, successful_test_case):
    """Test async measure method."""
    score = await niah_metric.a_measure(successful_test_case)
    assert score == 1
