# This file will be imported by all test files
import os
from dotenv import load_dotenv


def pytest_configure(config):
    # This will run once per test run
    # before tests are collected or executed

    load_dotenv()

    os.environ["COWABUNGA_API_KEY"] = os.environ.get("COWABUNGA_API_KEY", "mock-data")
    os.environ["COWABUNGA_API_URL"] = os.environ.get("COWABUNGA_API_URL", "https://cowabunga-api.uds.dev/openai/v1")
