# syntax=docker/dockerfile:1

# Turso/libSQL Server for CowabungaAI
# Replaces Supabase for simplified database operations

ARG BASE_IMAGE=debian:bookworm-slim
FROM ${BASE_IMAGE} AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Build libSQL from source (for latest features)
WORKDIR /build
RUN git clone --depth 1 https://github.com/tursodatabase/libsql.git . && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    make install

# Runtime stage
FROM ${BASE_IMAGE}

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy libSQL binaries from builder
COPY --from=builder /usr/local/bin/libsql-server /usr/local/bin/
COPY --from=builder /usr/local/lib/libsql* /usr/local/lib/

# Create non-root user
RUN useradd -r -s /bin/false turso

# Create data directory
RUN mkdir -p /data && chown turso:turso /data

# Copy migrations
COPY migrations/ /migrations/
RUN chown -R turso:turso /migrations

# Copy initialization script
COPY scripts/init-db.sh /init-db.sh
RUN chmod +x /init-db.sh && chown turso:turso /init-db.sh

# Switch to non-root user
USER turso

# Set environment variables
ENV TURSO_DATABASE_PATH=/data/cowabunga.db \
    TURSO_LISTEN_ADDR=0.0.0.0:8080 \
    TURSO_AUTH_ENABLED=true

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Initialize database on first run
RUN /init-db.sh

# Start libSQL server
CMD ["libsql-server", "--db-path", "${TURSO_DATABASE_PATH}", "--listen-addr", "${TURSO_LISTEN_ADDR}"]
