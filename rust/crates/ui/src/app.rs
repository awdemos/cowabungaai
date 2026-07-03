//! Root Leptos application component.

use leptos::prelude::*;

#[component]
pub fn App() -> impl IntoView {
    view! {
        <main>
            <h1>"CowabungaAI"</h1>
            <p>"Rust rewrite in progress."</p>
        </main>
    }
}
