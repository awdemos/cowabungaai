ARG LOCAL_VERSION=0bf35225
ARG SDK_REGISTRY=ghcr.io

# Builder: the SDK image carries the wheelhouse with cowabunga_sdk and its deps.
FROM ${SDK_REGISTRY}/defenseunicorns/cowabungaai/cowabunga-sdk:${LOCAL_VERSION} AS builder
USER root
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-index --find-links=/cowabungaai/src/cowabunga_sdk/build cowabunga_sdk grpcio grpcio-tools protobuf grpcio-reflection grpcio-health-checking confz click && \
    python -m pip uninstall -y pip setuptools wheel

# Runtime: slim python image instead of the full SDK toolchain image.
FROM ghcr.io/defenseunicorns/leapfrogai/python:3.11 AS runtime
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=builder /opt/venv /opt/venv
# --chmod: build contexts with a restrictive umask (e.g. 0077 checkouts) would
# otherwise preserve 0600 modes and the non-root runtime user couldn't read these.
COPY --chmod=644 main.py /app/main.py
COPY --chmod=644 config.yaml /app/config.yaml
ENV COWABUNGA_CONFIG_FILE=/app/config.yaml
ENV COWABUNGA_APP=/app/main.py
EXPOSE 50051
# import_app needs a "module:object" spec and a sys.path entry (--app-dir),
# not a filesystem path.
ENTRYPOINT ["lfai-cli", "--app-dir=/app", "main:Model"]
