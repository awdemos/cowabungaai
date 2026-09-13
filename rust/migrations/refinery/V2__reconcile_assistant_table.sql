-- Reconcile table name with the CRUD layer, which expects `assistant_objects`.
-- The initial schema used `assistant`; this migration creates the alias table
-- used by the API and migrates any existing rows.
CREATE TABLE IF NOT EXISTS assistant_objects (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'assistant',
    created_at INTEGER DEFAULT 0,
    name TEXT,
    description TEXT,
    model TEXT NOT NULL,
    instructions TEXT,
    tools TEXT DEFAULT '[]',
    tool_resources TEXT DEFAULT '{}',
    metadata TEXT DEFAULT '{}',
    temperature REAL,
    top_p REAL,
    response_format TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_assistant_objects_user ON assistant_objects(user_id);

-- Copy any rows created against the old table name.
INSERT OR IGNORE INTO assistant_objects
SELECT * FROM assistant;
