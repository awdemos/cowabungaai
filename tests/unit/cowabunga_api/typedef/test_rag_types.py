"""Tests for RAG typedef module."""

import pytest
from cowabunga_api.typedef.rag.rag_types import ConfigurationSingleton, ConfigurationPayload


def test_configuration_singleton_instance():
    """Test ConfigurationSingleton returns a ConfigurationPayload instance."""
    instance = ConfigurationSingleton.get_instance()
    assert isinstance(instance, ConfigurationPayload)
    assert instance.enable_reranking is True
    assert instance.rag_top_k_when_reranking == 100
    assert instance.ranking_model == "flashrank"


def test_configuration_payload_defaults():
    """Test ConfigurationPayload default values."""
    config = ConfigurationPayload()
    assert config.enable_reranking is None
    assert config.ranking_model is None
    assert config.rag_top_k_when_reranking is None


def test_configuration_payload_custom_values():
    """Test ConfigurationPayload with custom values."""
    config = ConfigurationPayload(
        enable_reranking=False,
        ranking_model="cross-encoder",
        rag_top_k_when_reranking=50,
    )
    assert config.enable_reranking is False
    assert config.ranking_model == "cross-encoder"
    assert config.rag_top_k_when_reranking == 50
