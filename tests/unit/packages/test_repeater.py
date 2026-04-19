"""Tests for the repeater package."""

import pytest
from cowabunga_sdk.llm import GenerationConfig, FinishReason
from packages.repeater.main import Model


def test_generation_config_defaults():
    """Test GenerationConfig can be instantiated with required fields."""
    config = GenerationConfig(
        max_new_tokens=100,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        do_sample=True,
        n=1,
        stop=["\n"],
        repetition_penalty=1.0,
        presence_penalty=0.0,
        best_of="",
        logit_bias={},
        return_full_text=False,
        truncate=0,
        typical_p=1.0,
        watermark=False,
        seed=42,
    )
    assert config.max_new_tokens == 100
    assert config.temperature == 0.7


def test_finish_reason_enum_values():
    """Test FinishReason enum has expected values."""
    assert FinishReason.NONE.value == 0
    assert FinishReason.STOP.value == 1
    assert FinishReason.LENGTH.value == 2


@pytest.mark.asyncio
async def test_repeater_count_tokens():
    """Test the repeater model counts tokens as characters."""
    model = Model()
    result = await model.count_tokens("hello world")
    assert result == 11


@pytest.mark.asyncio
async def test_repeater_generate():
    """Test the repeater model echoes input characters."""
    model = Model()
    config = GenerationConfig(
        max_new_tokens=100,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        do_sample=True,
        n=1,
        stop=["\n"],
        repetition_penalty=1.0,
        presence_penalty=0.0,
        best_of="",
        logit_bias={},
        return_full_text=False,
        truncate=0,
        typical_p=1.0,
        watermark=False,
        seed=42,
    )
    chars = []
    async for char in model.generate("hi", config):
        chars.append(char)
    assert "".join(chars) == "hi"
