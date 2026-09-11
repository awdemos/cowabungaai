ARG LOCAL_VERSION=0bf35225
ARG SDK_REGISTRY=ghcr.io
FROM ${SDK_REGISTRY}/defenseunicorns/cowabungaai/cowabunga-sdk:0bf35225
USER root
RUN pip install --no-index --find-links=/cowabungaai/src/cowabunga_sdk/build cowabunga_sdk grpcio grpcio-tools protobuf grpcio-reflection grpcio-health-checking confz click
COPY main.py /app/main.py
COPY config.yaml /app/config.yaml
RUN chmod a+rX /app /app/main.py /app/config.yaml
ENV COWABUNGA_CONFIG_FILE=/app/config.yaml
ENV COWABUNGA_APP=/app/main.py
EXPOSE 50051
ENTRYPOINT ["lfai-cli", "/app/main.py"]
