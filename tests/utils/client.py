from urllib.parse import urljoin
from openai import OpenAI
import os
from requests import Response

import requests


def get_cowabunga_model() -> str:
    """Return the model to use for CowabungaAI (default: 'vllm')."""
    return os.getenv("COWABUNGA_MODEL", "vllm")


def get_openai_key() -> str:
    """Return the OpenAI API key or raise ValueError."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY not set")
    return api_key


def get_openai_model() -> str:
    """Return the OpenAI model (default: 'gpt-4o-mini')."""
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_cowabunga_api_key() -> str:
    """Return the CowabungaAI API key or raise ValueError."""
    api_key = os.getenv("COWABUNGA_API_KEY") or os.getenv("SUPABASE_USER_JWT")
    if api_key is None:
        raise ValueError("COWABUNGA_API_KEY or SUPABASE_USER_JWT not set")
    return api_key


def get_cowabunga_api_url() -> str:
    """Return the CowabungaAI API URL (default: 'https://cowabunga-api.uds.dev/openai/v1')."""
    return os.getenv("COWABUNGA_API_URL", "https://cowabunga-api.uds.dev/openai/v1")


def get_cowabunga_api_url_base() -> str:
    """Return the CowabungaAI API base URL, stripping '/openai/v1' if present."""
    url = os.getenv("COWABUNGA_API_URL", "https://cowabunga-api.uds.dev")
    if url.endswith("/openai/v1"):
        return url[:-9]
    return url


def openai_client() -> OpenAI:
    """Return an OpenAI client authenticated with OPENAI_API_KEY."""
    return OpenAI(api_key=get_openai_key())


def cowabunga_client() -> OpenAI:
    """Return an OpenAI-compatible client for the CowabungaAI API."""
    return OpenAI(
        base_url=get_cowabunga_api_url(),
        api_key=get_cowabunga_api_key(),
    )


class ClientConfig:
    """Configuration for a client that is OpenAI compliant."""

    client: OpenAI
    model: str

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model


def client_config_factory(client_name: str) -> ClientConfig:
    """Factory function for creating a client configuration that is OpenAI compliant."""
    if client_name == "openai":
        return ClientConfig(client=openai_client(), model=get_openai_model())
    elif client_name == "cowabunga":
        return ClientConfig(client=cowabunga_client(), model=get_cowabunga_model())
    else:
        raise ValueError(f"Unknown client name: {client_name}")


class CowabungaAIClient:
    """Client for handling queries in the CowabungaAI namespace that are not handled by the OpenAI SDK.

    Wraps the requests library to make HTTP requests to the CowabungaAI API.

    Raises:
        requests.HTTPError: If the response status code is not a 2xx status code.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or get_cowabunga_api_url_base()
        self.api_key = api_key or get_cowabunga_api_key()
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.get(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def post(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.post(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.put(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint, **kwargs) -> Response | None:
        url = urljoin(self.base_url, endpoint)
        response = requests.delete(url, headers=self.headers, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response) -> Response | None:
        response.raise_for_status()
        if response.content:
            return response
        return None
