//! Embedded SQL migrations run through libsql.

use std::collections::HashMap;

use crate::error::StorageError;

/// A single migration: version, name, and SQL body.
#[derive(Debug, Clone)]
pub struct Migration {
    pub version: String,
    pub name: String,
    pub sql: String,
}

/// All embedded migrations in version order.
pub fn migrations() -> Vec<Migration> {
    vec![
        Migration {
            version: "1".to_string(),
            name: "initial_schema".to_string(),
            sql: include_str!("../../../migrations/refinery/V1__initial_schema.sql").to_string(),
        },
        Migration {
            version: "2".to_string(),
            name: "reconcile_assistant_table".to_string(),
            sql: include_str!("../../../migrations/refinery/V2__reconcile_assistant_table.sql")
                .to_string(),
        },
    ]
}

/// Run migrations on a libsql connection, tracking applied versions in
/// `cowabunga_schema_migrations`.
pub async fn run_migrations(conn: &mut libsql::Connection) -> Result<Vec<String>, StorageError> {
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cowabunga_schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT
        )",
        (),
    )
    .await?;

    let applied: HashMap<String, ()> = {
        let mut rows = conn
            .query("SELECT version FROM cowabunga_schema_migrations", ())
            .await?;
        let mut map = HashMap::new();
        while let Some(row) = rows.next().await? {
            let version: String = row.get(0)?;
            map.insert(version, ());
        }
        map
    };

    let mut newly_applied = Vec::new();
    for migration in migrations() {
        if applied.contains_key(&migration.version) {
            continue;
        }

        conn.execute_batch(&migration.sql).await?;

        conn.execute(
            "INSERT INTO cowabunga_schema_migrations (version, name) VALUES (?, ?)",
            libsql::params![migration.version.clone(), migration.name.clone()],
        )
        .await?;

        newly_applied.push(migration.version.clone());
        tracing::info!(version = %migration.version, name = %migration.name, "applied migration");
    }

    Ok(newly_applied)
}
