ARG LOCAL_VERSION
FROM ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:${LOCAL_VERSION} AS sdk

FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11-dev AS builder

USER root
ARG SDK_DEST=src/leapfrogai_sdk/build

WORKDIR /cowabungaai

# create virtual environment for light-weight portability and minimal libraries
RUN python3.11 -m venv .venv
ENV PATH="/cowabungaai/.venv/bin:$PATH"

COPY --from=sdk /cowabungaai/${SDK_DEST} ${SDK_DEST}
COPY packages/whisper packages/whisper

RUN rm -f packages/whisper/build/*.whl &&\
    python -m pip wheel "packages/whisper[dev]" -w packages/whisper/build --find-links=${SDK_DEST} &&\
    pip install packages/whisper/build/lfai_whisper*.whl --no-index --find-links=packages/whisper/build/

# Use hardened ffmpeg image to get compiled binaries
FROM cgr.dev/chainguard/ffmpeg:latest AS ffmpeg

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

COPY --from=ffmpeg /usr/bin/ffmpeg /usr/bin
COPY --from=ffmpeg /usr/bin/ffprobe /usr/bin
COPY --from=ffmpeg /usr/lib/lib* /usr/lib

COPY --from=builder /cowabungaai/.venv/ /cowabungaai/.venv/

# set the path to the cuda 11.8 dependencies
ENV LD_LIBRARY_PATH \
/cowabungaai/.venv/lib64/python3.11/site-packages/nvidia/cublas/lib:\
/cowabungaai/.venv/lib64/python3.11/site-packages/nvidia/cudnn/lib

COPY packages/whisper/main.py .

EXPOSE 50051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50051/health || exit 1

ENTRYPOINT ["python", "-u", "main.py"]
