ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder
ARG SDK_DEST=src/leapfrogai_sdk/build
USER root
WORKDIR /cowabungaai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

# copy and install all python dependencies
# NOTE: We are copying the cowabungaai whl to this filename because installing 'optional extras' from
#       a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/text-embeddings packages/text-embeddings

RUN rm -f packages/text-embeddings/build/*.whl && \
    python -m pip wheel packages/text-embeddings -w packages/text-embeddings/build --find-links=${SDK_DEST} && \
    pip install packages/text-embeddings/build/lfai_text_embeddings*.whl --no-index --find-links=packages/text-embeddings/build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime

ENV PATH="/cowabungaai/.venv/bin:$PATH"

WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI Text Embeddings Backend"
LABEL org.opencontainers.image.description="Text embedding generation service for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

COPY packages/text-embeddings/main.py .

EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

ENTRYPOINT ["python", "-u", "main.py"]
