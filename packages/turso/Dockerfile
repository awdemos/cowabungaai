# Turso/libSQL Server for CowabungaAI
# Simplified version using SQLite with HTTP API

FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    aiosqlite \
    fastapi \
    uvicorn

# Create non-root user
RUN useradd -r -s /bin/false turso

# Create directories
RUN mkdir -p /data /migrations /scripts

# Copy migrations
COPY migrations/ /migrations/

# Copy initialization script
COPY scripts/init-db.sh /scripts/init-db.sh
RUN chmod +x /scripts/init-db.sh

# Copy API server
COPY api.py /app.py

RUN chown -R turso:turso /data /migrations /scripts /app.py && \
    chmod 755 /scripts/init-db.sh && \
    chmod 644 /migrations/*.sql && \
    chmod 644 /app.py

# Switch to non-root user
USER turso

# Set environment variables
ENV TURSO_DATABASE_PATH=/data/cowabunga.db \
    TURSO_LISTEN_ADDR=0.0.0.0:8080 \
    TURSO_AUTH_ENABLED=true

# Expose port
EXPOSE 8080

# Initialize database on startup
CMD ["/bin/bash", "-c", "/scripts/init-db.sh && python /app.py"]
