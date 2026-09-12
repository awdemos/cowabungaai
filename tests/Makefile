LEAPFROGAI_MODEL ?= llama-cpp-python
COWABUNGA_RUN_NIAH_TESTS ?= false
COWABUNGA_RUN_REPEATER_TESTS ?= true

install:
	pip install ".[dev]" "legacy/cowabunga_api" "legacy/cowabunga_sdk" "legacy/cowabunga_evals" "packages/repeater"

test-api-unit:
	COWABUNGA_RUN_REPEATER_TESTS=$(COWABUNGA_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/unit
	COWABUNGA_RUN_REPEATER_TESTS=$(COWABUNGA_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/pytest

test-load:
	python -m locust -f $$(pwd)/tests/load/loadtest.py --web-port 8089

test-conformance:
	PYTHONPATH=$$(pwd) pytest -vv -s tests/conformance
