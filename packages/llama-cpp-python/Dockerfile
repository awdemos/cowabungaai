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

# copy the llama-cpp-python build dependencies over
# NOTE: We are copying to this filename because installing 'optional extras' from a wheel requires the absolute path to the wheel file (instead of a wildcard whl)
COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/llama-cpp-python packages/llama-cpp-python

RUN rm -f packages/llama-cpp-python/build/*.whl && \
    python -m pip wheel packages/llama-cpp-python -w packages/llama-cpp-python/build --find-links=${SDK_DEST}

RUN pip install packages/llama-cpp-python/build/lfai_llama_cpp_python*.whl --no-index --find-links=packages/llama-cpp-python/build/

# Prepare an empty /data/.model directory in the builder stage so the
# runtime stage (which has no shell) can copy it in.
RUN mkdir -p /data/.model && touch /data/.model/.keep

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime

ENV PATH="/cowabungaai/.venv/bin:$PATH"

WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI LLaMA C++ Python Backend"
LABEL org.opencontainers.image.description="CPU-based LLM inference backend using llama-cpp-python for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

# The runtime image is a minimal Wolfi Python image and lacks libgomp, which
# llama-cpp-python's libllama.so requires.
COPY --from=builder /usr/lib/libgomp.so.1 /usr/lib/libgomp.so.1
COPY --from=builder /usr/lib/libgomp.so.1.0.0 /usr/lib/libgomp.so.1.0.0
COPY --from=builder /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6
COPY --from=builder /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1

# Model weights are mounted here at runtime (PVC in K8s, volume in Docker).
COPY --from=builder /data/.model /data/.model

# --chmod: build contexts with a restrictive umask (e.g. 0077 checkouts) would
# otherwise preserve 0600 modes and the non-root runtime user couldn't read these.
COPY --chmod=644 packages/llama-cpp-python/main.py .
COPY --chmod=644 packages/llama-cpp-python/config.yaml .

EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

ENTRYPOINT ["python", "-m", "cowabunga_sdk.cli", "--app-dir=.", "main:Model"]
