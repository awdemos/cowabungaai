ARG LOCAL_VERSION
ARG SDK_REGISTRY=ghcr.io
FROM ${SDK_REGISTRY}/defenseunicorns/cowabungaai/cowabunga-sdk:${LOCAL_VERSION} AS sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

USER root
ARG SDK_DEST=src/cowabunga_sdk/build

WORKDIR /cowabungaai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"
RUN pip install --upgrade "pip<24" "setuptools<71" wheel pybind11 Cython

COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/whisper packages/whisper

# WHISPER_EXTRAS: wheel extras to build with. Default [dev] preserves the original
# GPU/CI build; pass WHISPER_EXTRAS= (empty) for a CPU image without the torch dev stack.
ARG WHISPER_EXTRAS="[dev]"
RUN rm -f packages/whisper/build/*.whl &&\
    python -m pip wheel "packages/whisper${WHISPER_EXTRAS}" -w packages/whisper/build --find-links=${SDK_DEST} --no-build-isolation &&\
    pip install packages/whisper/build/lfai_whisper*.whl --no-index --find-links=packages/whisper/build/ &&\
    python -m pip uninstall -y pip setuptools wheel Cython pybind11

# hardened and slim python image
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime

ENV PATH="/cowabungaai/.venv/bin:$PATH"

WORKDIR /cowabungaai

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI Whisper Backend"
LABEL org.opencontainers.image.description="Speech-to-text processing service using Whisper for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

# faster-whisper decodes audio through PyAV (bundled in the venv as av.libs);
# the ffmpeg/ffprobe binaries and codec libraries are not used by main.py.
COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

# set the path to the cuda 11.8 dependencies
ENV LD_LIBRARY_PATH=\
/cowabungaai/.venv/lib64/python3.11/site-packages/nvidia/cublas/lib:\
/cowabungaai/.venv/lib64/python3.11/site-packages/nvidia/cudnn/lib

# --chmod: build contexts with a restrictive umask (e.g. 0077 checkouts) would
# otherwise preserve 0600 modes and the non-root runtime user couldn't read these.
COPY --chmod=644 packages/whisper/main.py .

EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

ENTRYPOINT ["python", "-u", "main.py"]
