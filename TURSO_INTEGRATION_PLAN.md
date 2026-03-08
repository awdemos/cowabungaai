# Turso Integration Plan for CowabungaAI

## Overview
Replace Supabase with Turso (libSQL/SQLite-based database) to reduce complexity in CowabungaAI.

## Why Turso Instead of Supabase

### Current Supabase Stack (Complex)
- PostgreSQL database
- Kong API gateway
- GoTrue authentication
- PostgREST API
- Realtime subscriptions
- Storage service
- Multiple containers (10+ pods)

### Turso Stack (Simple)
- SQLite/libSQL database
- Edge-compatible
- Single database service
- Embedded-first architecture
- Fewer moving parts

## Benefits

1. **Reduced Complexity**
   - Single database vs 10+ microservices
   - Simpler deployment
   - Fewer failure points
   - Easier local development

2. **Performance**
   - SQLite is faster for read-heavy workloads
   - No network overhead for embedded mode
   - Edge-optimized

3. **Resource Efficiency**
   - Lower memory footprint
   - Fewer CPU requirements
   - Smaller container images

4. **Developer Experience**
   - Familiar SQLite syntax
   - Easier debugging
   - Simpler backup/restore

## Integration Plan

### Phase 1: Preparation (Current Worktree)
**Status:** Complete current changes first
- [ ] Finish CowabungaAI CPU deployment (API, UI, Llama)
- [ ] Push changes to remote
- [ ] Create new worktree for Turso integration

### Phase 2: Research & Design (New Worktree: `turso-integration`)

```bash
# Create worktree
git worktree add ../cowabungaai-turso -b turso-integration
cd ../cowabungaai-turso

# Install Turso CLI
curl -sSfL https://get.turso.tech/install.sh | bash

# Research Turso integration
turso --help
```

**Tasks:**
1. **Evaluate Turso Features**
   - libSQL API compatibility
   - Edge functions support
   - Authentication methods
   - Migration from PostgreSQL

2. **API Compatibility**
   - Compare Supabase API vs Turso API
   - Identify breaking changes
   - Design abstraction layer

3. **Data Migration**
   - PostgreSQL to SQLite schema conversion
   - Data migration scripts
   - Test with sample data

### Phase 3: Implementation (Weeks 1-3)

#### Week 1: Turso Package Creation

```
packages/turso/
├── Dockerfile          # Turso/libSQL server
├── zarf.yaml           # Zarf package definition
├── chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       └── pvc.yaml
├── migrations/         # SQLite migrations
│   ├── 001_initial_schema.sql
│   └── 002_add_indexes.sql
└── README.md
```

**Dockerfile:**
```dockerfile
FROM ghcr.io/tursodatabase/libsql-server:latest

# Copy migrations
COPY migrations/ /migrations/

# Initialize database
RUN sqlite3 /data/cowabunga.db < /migrations/001_initial_schema.sql

EXPOSE 8080
CMD ["libsql-server", "--db-path", "/data/cowabunga.db"]
```

**zarf.yaml:**
```yaml
kind: ZarfPackageConfig
metadata:
  name: turso
  description: Turso/libSQL database for CowabungaAI

components:
  - name: turso
    required: true
    charts:
      - name: turso
        version: 0.1.0
        namespace: leapfrogai
        localPath: chart
    images:
      - ghcr.io/tursodatabase/libsql-server:latest
```

#### Week 2: API Adaptation

**Modify leapfrogai_api:**

1. **Database Abstraction Layer**
   ```python
   # src/leapfrogai_api/database/
   ├── __init__.py
   ├── base.py           # Abstract database interface
   ├── supabase.py       # Current Supabase implementation
   └── turso.py          # New Turso implementation
   ```

2. **Configuration**
   ```python
   # src/leapfrogai_api/config.py
   class DatabaseType(Enum):
       SUPABASE = "supabase"
       TURSO = "turso"
   
   DATABASE_TYPE = os.getenv("DATABASE_TYPE", "supabase")
   ```

3. **Environment Variables**
   ```yaml
   # packages/api/values.yaml
   env:
     DATABASE_TYPE: turso
     TURSO_URL: turso.leapfrogai.svc.cluster.local:8080
     TURSO_AUTH_TOKEN: {{ .Values.turso.authToken }}
   ```

#### Week 3: Testing & Validation

1. **Unit Tests**
   - Database operations
   - Migration scripts
   - API compatibility

2. **Integration Tests**
   - Deploy with Turso
   - Test API endpoints
   - Verify UI functionality

3. **Performance Tests**
   - Compare query performance
   - Measure resource usage
   - Load testing

### Phase 4: Migration Guide (Week 4)

**For existing users:**

```bash
# Export from Supabase
pg_dump -h supabase-postgresql -U postgres > backup.sql

# Convert to SQLite
python3 scripts/pg-to-sqlite.py backup.sql > turso.sql

# Import to Turso
sqlite3 /data/cowabunga.db < turso.sql

# Update deployment
kubectl set env deployment/leapfrogai-api DATABASE_TYPE=turso
```

### Phase 5: Rollout Strategy

1. **Parallel Deployment**
   - Deploy Turso alongside Supabase
   - A/B test with feature flags
   - Gradual traffic migration

2. **Feature Parity Checklist**
   - [ ] User authentication
   - [ ] Chat history storage
   - [ ] File metadata
   - [ ] RAG embeddings (if using text-embeddings)
   - [ ] API key management

3. **Rollback Plan**
   - Keep Supabase package available
   - Document rollback procedure
   - Maintain backward compatibility

## Technical Considerations

### Authentication
**Supabase:** GoTrue (JWT-based)
**Turso:** Custom auth or integrate with:
- Keycloak (already in UDS)
- Authentik
- Custom JWT service

### Real-time Features
**Supabase:** Built-in realtime subscriptions
**Turso:** Use alternatives:
- Server-Sent Events (SSE)
- WebSockets
- Polling (simpler)

### Storage
**Supabase:** Object storage service
**Turso:** Use alternatives:
- MinIO (S3-compatible)
- Local persistent volumes
- External object storage

### Edge Functions
**Supabase:** Edge functions
**Turso:** Use alternatives:
- Kubernetes Jobs
- CronJobs
- External functions service

## Database Schema

### Core Tables (SQLite)

```sql
-- Users and authentication
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON
);

-- Chat conversations
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id),
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT REFERENCES conversations(id),
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API keys
CREATE TABLE api_keys (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id),
    key_hash TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- File metadata (if using object storage)
CREATE TABLE files (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id),
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    size INTEGER,
    mime_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_files_user ON files(user_id);
```

## Configuration Changes

### Environment Variables

```bash
# Old (Supabase)
SUPABASE_URL=https://supabase.example.com
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# New (Turso)
DATABASE_TYPE=turso
TURSO_URL=turso.leapfrogai.svc.cluster.local:8080
TURSO_AUTH_TOKEN=xxx
```

### Helm Values

```yaml
# packages/api/values.yaml
database:
  type: turso  # or supabase
  
turso:
  enabled: true
  url: turso.leapfrogai.svc.cluster.local:8080
  authToken: ""
  storage:
    size: 10Gi
    class: local-path
```

## Success Criteria

- [ ] Turso package builds and deploys
- [ ] All API endpoints work with Turso
- [ ] UI functions correctly
- [ ] Performance matches or exceeds Supabase
- [ ] Resource usage reduced by 50%+
- [ ] Deployment time reduced by 60%+
- [ ] Migration guide complete
- [ ] Backward compatibility maintained

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Data loss during migration | Comprehensive backup strategy, dry-run mode |
| Feature incompatibility | Abstraction layer, feature flags |
| Performance regression | Benchmark testing, query optimization |
| User authentication changes | Integrate with Keycloak (UDS standard) |

## Timeline

- **Week 1:** Research, design, Turso package creation
- **Week 2:** API adaptation, database abstraction layer
- **Week 3:** Testing, validation, performance benchmarks
- **Week 4:** Documentation, migration guide
- **Week 5:** Gradual rollout, monitoring
- **Week 6:** Stabilization, feedback collection

Total: **6 weeks** to full Turso integration

## Next Steps

1. **Complete current work** (API, UI, Llama deployment)
2. **Push changes** to remote repository
3. **Create worktree:** `git worktree add ../cowabungaai-turso -b turso-integration`
4. **Begin Phase 2:** Research & Design

## Resources

- Turso Documentation: https://docs.turso.tech/
- libSQL GitHub: https://github.com/tursodatabase/libsql
- SQLite to PostgreSQL Migration: https://www.sqlite.org/pgdiff.html
- Turso CLI: https://github.com/tursodatabase/turso-cli

---

*Created: 2026-03-08*
*Status: Planning phase, awaiting current work completion*
*Worktree: To be created after current changes pushed*
