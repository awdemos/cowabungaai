from openai import OpenAI
import pytest

from tests.utils.client import cowabunga_client, get_cowabunga_model


@pytest.fixture(scope="module")
def client() -> OpenAI:
    return cowabunga_client()


@pytest.fixture(scope="module")
def model_name() -> str:
    return get_cowabunga_model()
