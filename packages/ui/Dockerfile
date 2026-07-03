ARG LOCAL_VERSION
FROM rust:1.85 AS builder

RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

WORKDIR /cowabungaai

COPY rust/Cargo.toml rust/Cargo.lock rust/rust-toolchain.toml ./
COPY rust/crates ./crates
COPY rust/proto ./proto
COPY rust/migrations ./migrations
COPY rust/.cargo ./.cargo
COPY rust/deny.toml ./

RUN cargo build -p cowabunga-ui --release

FROM cgr.dev/chainguard/glibc-dynamic:latest AS runtime

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI UI"
LABEL org.opencontainers.image.description="Rust/Leptos SSR web UI for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/target/release/cowabunga-ui /usr/local/bin/cowabunga-ui

ENV LEPTOS_SITE_ADDR=0.0.0.0:3000
ENV LEPTOS_OUTPUT_NAME=cowabunga-ui

EXPOSE 3000

ENTRYPOINT ["/usr/local/bin/cowabunga-ui"]
