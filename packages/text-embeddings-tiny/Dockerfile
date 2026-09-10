# Tiny text-embeddings: ONNX MiniLM + onnxruntime-cpu (no torch).
# ~350MB image vs ~5.75GB for the torch/InstructorEmbedding variant.
ARG LOCAL_VERSION
ARG SDK_REGISTRY=ghcr.io
FROM ${SDK_REGISTRY}/defenseunicorns/cowabungaai/cowabunga-sdk:${LOCAL_VERSION} AS sdk

# hardened and slim python w/ developer tools image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder
ARG SDK_DEST=src/cowabunga_sdk/build
USER root
WORKDIR /cowabungaai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

# copy and install all python dependencies
COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/text-embeddings-tiny packages/text-embeddings-tiny

RUN rm -f packages/text-embeddings-tiny/build/*.whl && \
    python -m pip install --no-cache-dir "onnxruntime==1.18.1" "numpy==1.26.4" "tokenizers==0.19.1" "huggingface_hub==0.25.1" && \
    python -m pip wheel packages/text-embeddings-tiny -w packages/text-embeddings-tiny/build --find-links=${SDK_DEST} && \
    pip install packages/text-embeddings-tiny/build/lfai_text_embeddings_tiny*.whl --no-index --find-links=packages/text-embeddings-tiny/build/

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime

ENV PATH="/cowabungaai/.venv/bin:$PATH"

WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI Text Embeddings Backend (Tiny)"
LABEL org.opencontainers.image.description="MiniLM ONNX embedding backend for CowabungaAI (~400MB, no torch)"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --chown=65532:65532 --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

COPY --chown=65532:65532 packages/text-embeddings-tiny/main_tiny.py .

ENV COWABUNGA_MODEL_PATH=/data/.model

EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

ENTRYPOINT ["python", "-u", "main_tiny.py"]
