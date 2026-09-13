//! Model registry and configuration loading.

use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Clone, Deserialize)]
pub struct Model {
    pub name: String,
    pub backend: String,
}

#[derive(Debug, Default)]
pub struct ModelRegistry {
    models: HashMap<String, Model>,
}

impl ModelRegistry {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn get(&self, name: &str) -> Option<&Model> {
        self.models.get(name)
    }

    pub fn len(&self) -> usize {
        self.models.len()
    }

    pub fn is_empty(&self) -> bool {
        self.models.is_empty()
    }

    pub fn iter(&self) -> impl Iterator<Item = &Model> {
        self.models.values()
    }

    pub fn add(&mut self, model: Model) {
        self.models.insert(model.name.clone(), model);
    }
}
