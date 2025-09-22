ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/cowabungaai-sdk:${LOCAL_VERSION} AS sdk

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

ARG SDK_DEST=src/leapfrogai_sdk/build

USER root

WORKDIR /cowabungaai

COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/repeater packages/repeater

# create virtual environment for light-weight portability and minimal libraries
RUN python -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

RUN rm -f packages/repeater/build/*.whl && \
    python -m pip wheel packages/repeater -w packages/repeater/build --find-links=${SDK_DEST} && \
    pip install packages/repeater/build/lfai_repeater*.whl --no-index --find-links=packages/repeater/build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime

ENV PATH="/cowabungaai/.venv/bin:$PATH"

WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI Repeater Backend"
LABEL org.opencontainers.image.description="Testing/echo backend service for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/
COPY packages/repeater/main.py .
COPY packages/repeater/config.yaml .

# Publish port
EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

# Run the repeater model
ENTRYPOINT ["python", "-m", "leapfrogai_sdk.cli", "--app-dir=.", "main:Model"]
