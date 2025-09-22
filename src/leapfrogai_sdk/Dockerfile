FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

ARG SDK_DEST=src/leapfrogai_sdk/build

USER root

WORKDIR /cowabungaai

COPY ./src/leapfrogai_sdk /cowabungaai/src/leapfrogai_sdk

RUN python -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

RUN rm -f ${SDK_DEST}/*.whl && \
    python -m pip wheel src/leapfrogai_sdk -w ${SDK_DEST}

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI SDK"
LABEL org.opencontainers.image.description="gRPC SDK and protocol buffers for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"
