LEAPFROGAI_MODEL ?= llama-cpp-python
LFAI_RUN_NIAH_TESTS ?= false
LFAI_RUN_REPEATER_TESTS ?= true

install:
	pip install ".[dev]" "src/cowabunga_api" "src/cowabunga_sdk" "packages/repeater"

test-api-unit:
	LFAI_RUN_REPEATER_TESTS=$(LFAI_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/unit
	LFAI_RUN_REPEATER_TESTS=$(LFAI_RUN_REPEATER_TESTS) PYTHONPATH=$$(pwd) python -m pytest -vv -s tests/pytest

test-load:
	python -m locust -f $$(pwd)/tests/load/loadtest.py --web-port 8089

test-conformance:
	PYTHONPATH=$$(pwd) pytest -vv -s tests/conformance
