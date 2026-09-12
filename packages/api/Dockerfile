ARG LOCAL_VERSION

# --- dependency planner: captures the workspace dependency graph only -------
FROM lukemathwalker/cargo-chef:0.1.71-rust-1.85-bookworm AS planner
WORKDIR /cowabungaai
COPY rust/Cargo.toml rust/Cargo.lock ./
COPY rust/crates ./crates
RUN cargo chef prepare --recipe-path recipe.json

# --- dependency builder: compiles crates.io deps once, cached across --------
# --- source-only changes -----------------------------------------------------
FROM lukemathwalker/cargo-chef:0.1.71-rust-1.85-bookworm AS builder
RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*
WORKDIR /cowabungaai
COPY --from=planner /cowabungaai/recipe.json recipe.json
# Cook only the dependencies: this layer is invalidated solely by manifest
# changes, so editing crate source does not recompile the dependency graph.
RUN cargo chef cook --release --recipe-path recipe.json
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
# Ship the lockfile so image SBOM scanners (syft) can attribute crate-level deps
# to the statically stripped binary.
COPY --from=builder /cowabungaai/Cargo.lock /usr/local/share/cowabunga/Cargo.lock

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/cowabunga-api"]
