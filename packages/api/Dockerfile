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

RUN cargo build -p cowabunga-api --release

FROM cgr.dev/chainguard/glibc-dynamic:latest AS runtime

# Add CowabungaAI labels
LABEL org.opencontainers.image.title="CowabungaAI API"
LABEL org.opencontainers.image.description="Rust API backend with OpenAI-compatible endpoints for CowabungaAI"
LABEL org.opencontainers.image.vendor="CowabungaAI"
LABEL org.opencontainers.image.authors="CowabungaAI Team"
LABEL org.opencontainers.image.source="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.documentation="https://github.com/awdemos/cowabungaai"
LABEL org.opencontainers.image.licenses="BSL-1.1"
LABEL org.opencontainers.image.version="0.14.0"
LABEL maintainer="CowabungaAI Team"

COPY --from=builder /cowabungaai/target/release/cowabunga-api /usr/local/bin/cowabunga-api

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/cowabunga-api"]
