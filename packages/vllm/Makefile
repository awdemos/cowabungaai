ARCH ?= amd64
LOCAL_VERSION ?= $(shell git rev-parse --short HEAD)
DOCKER_FLAGS :=

install:
	python -m pip install ../../src/cowabunga_sdk
	python -m pip install -e ".[dev]"

download:
	@env $$(cat .env | xargs) python src/model_download.py

dev: download
	@env $$(cat .env | xargs) python -m cowabunga_sdk.cli --app-dir=src/ main:Model

docker: download
	docker build ${DOCKER_FLAGS} \
		--platform=linux/${ARCH} \
		--build-arg LOCAL_VERSION=${LOCAL_VERSION} \
		--build-arg COMPONENT_DIRECTORY="./" \
		-t ghcr.io/defenseunicorns/cowabungaai/vllm:${LOCAL_VERSION} \
		-f ./Dockerfile .

	docker run -it --rm \
		--env-file ./.env \
		-v $(PWD)/config.yaml:/home/cowabungaai/config.yaml \
		-v $(PWD)/.model:/home/cowabungaai/.model \
		ghcr.io/defenseunicorns/cowabungaai/vllm:${LOCAL_VERSION}
