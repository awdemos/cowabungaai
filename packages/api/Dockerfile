ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

ARG SDK_DEST=src/leapfrogai_sdk/build

USER root

WORKDIR /cowabungaai

# copy the api dependencies over
COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY src/leapfrogai_api src/leapfrogai_api

RUN python -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

RUN rm -f packages/api/build/*.whl && \
    python -m pip wheel src/leapfrogai_api -w packages/api/build --find-links=${SDK_DEST} && \
    pip install packages/api/build/leapfrogai_api*.whl --no-index --find-links=packages/api/build/

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime
ENV PATH="/cowabungaai/.venv/bin:$PATH"
WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI API"
LABEL org.opencontainers.image.description="FastAPI backend with OpenAI-compatible endpoints for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["uvicorn", "leapfrogai_api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug"]
