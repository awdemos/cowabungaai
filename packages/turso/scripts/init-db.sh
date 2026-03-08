#!/bin/bash
set -e

# Initialize Turso database for CowabungaAI
# This script runs on first startup to set up the database

echo "Initializing CowabungaAI database..."

# Wait for database to be ready
sleep 2

# Check if database exists
if [ ! -f "${TURSO_DATABASE_PATH}" ]; then
    echo "Creating new database..."
    sqlite3 "${TURSO_DATABASE_PATH}" "SELECT 1;"
fi

# Apply migrations
echo "Applying migrations..."
for migration in /migrations/*.sql; do
    if [ -f "$migration" ]; then
        echo "Applying migration: $(basename $migration)"
        sqlite3 "${TURSO_DATABASE_PATH}" < "$migration" || {
            echo "Error applying migration: $(basename $migration)"
            exit 1
        }
    fi
done

echo "Database initialization complete!"

# Verify database
echo "Verifying database schema..."
TABLE_COUNT=$(sqlite3 "${TURSO_DATABASE_PATH}" "SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
echo "Database has $TABLE_COUNT tables"

# Show schema version
VERSION=$(sqlite3 "${TURSO_DATABASE_PATH}" "SELECT version FROM schema_migrations ORDER BY applied_at DESC LIMIT 1;" 2>/dev/null || echo "unknown")
echo "Schema version: $VERSION"

exit 0
