# Turso Database Package for CowabungaAI

## Overview
This package replaces Supabase with Turso (libSQL/SQLite) to reduce deployment complexity.

## Why Turso?

### Supabase Complexity (Current)
- 10+ microservices (PostgreSQL, Kong, GoTrue, PostgREST, etc.)
- Complex authentication flow
- Heavy resource requirements
- Long deployment times

### Turso Simplicity (New)
- Single SQLite/libSQL server
- Embedded-first architecture
- Lightweight resource footprint
- Fast deployment

## Features
- ✅ SQLite/libSQL database server
- ✅ HTTP API for database operations
- ✅ Edge-compatible
- ✅ Built-in authentication support
- ✅ Simple backup/restore
- ✅ Migration support

## Quick Start

### Local Development
```bash
# Run Turso server locally
docker run -d \
  --name turso \
  -p 8080:8080 \
  -v turso-data:/data \
  ghcr.io/tursodatabase/libsql-server:latest

# Connect to database
sqlite3 http://localhost:8080
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f https://raw.githubusercontent.com/awdemos/cowabungaai/main/packages/turso/chart/

# Or with Helm
helm install turso ./packages/turso/chart -n cowabunga
```

## Configuration

### Environment Variables
```bash
TURSO_URL=turso.cowabunga.svc.cluster.local:8080
TURSO_AUTH_TOKEN=your-auth-token
TURSO_DATABASE_PATH=/data/cowabunga.db
```

### Helm Values
```yaml
# values.yaml
replicaCount: 1

image:
  repository: ghcr.io/tursodatabase/libsql-server
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

persistence:
  enabled: true
  size: 10Gi
  storageClass: local-path

auth:
  enabled: true
  existingSecret: turso-auth
```

## Database Schema

See `migrations/` directory for complete schema:
- `001_initial_schema.sql` - Core tables
- `002_add_indexes.sql` - Performance indexes
- `003_add_constraints.sql` - Data integrity

## API Compatibility

### With Supabase
```python
# Old (Supabase)
from supabase import create_client
supabase = create_client(url, key)
result = supabase.table('users').select('*').execute()

# New (Turso)
from turso import TursoClient
turso = TursoClient(url, token)
result = turso.execute('SELECT * FROM users')
```

### With CowabungaAPI
```python
# API will auto-detect database type
# No code changes needed!
from cowabunga_api import app  # Works with both
```

## Migration from Supabase

See `scripts/migrate-from-supabase.sh` for automated migration.

## Resources
- [Turso Documentation](https://docs.turso.tech/)
- [libSQL GitHub](https://github.com/tursodatabase/libsql)
- [Migration Guide](./MIGRATION.md)

## Status
🚧 **In Development** - See [TURSO_INTEGRATION_PLAN.md](../../TURSO_INTEGRATION_PLAN.md) for timeline.
