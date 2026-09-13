"""Tests for vector store search typedefs."""

import pytest
from cowabunga_api.typedef.vectorstores.search_types import Vector, SearchItem, SearchResponse


def test_vector_creation():
    """Test Vector model can be instantiated."""
    vector = Vector(
        vector_store_id="vs-1",
        file_id="file-1",
        content="test content",
        metadata={"source": "test"},
        embedding=[0.1, 0.2, 0.3],
    )
    assert vector.vector_store_id == "vs-1"
    assert vector.embedding == [0.1, 0.2, 0.3]


def test_search_item_defaults():
    """Test SearchItem default values."""
    item = SearchItem(
        id="item-1",
        vector_store_id="vs-1",
        file_id="file-1",
        content="test",
        metadata={},
        similarity=0.95,
    )
    assert item.rank is None
    assert item.score is None


def test_search_item_with_ranking():
    """Test SearchItem with rank and score."""
    item = SearchItem(
        id="item-1",
        vector_store_id="vs-1",
        file_id="file-1",
        content="test",
        metadata={},
        similarity=0.95,
        rank=1,
        score=0.98,
    )
    assert item.rank == 1
    assert item.score == 0.98


def test_search_response():
    """Test SearchResponse can be created."""
    response = SearchResponse(
        data=[
            SearchItem(
                id="item-1",
                vector_store_id="vs-1",
                file_id="file-1",
                content="test",
                metadata={},
                similarity=0.95,
            ),
        ]
    )
    assert len(response.data) == 1
    assert response.data[0].id == "item-1"
