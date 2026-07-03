install:
	python -m pip install ../../legacy/cowabunga_sdk
	python -m pip install -e ".[dev]"


dev:
	make install
	python -m cowabunga_sdk.cli --app-dir=. main:Model
