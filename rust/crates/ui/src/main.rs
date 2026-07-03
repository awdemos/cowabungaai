//! CowabungaAI UI server entry point (Leptos SSR on Axum).

use axum::{
    Router,
    body::Body,
    extract::State,
    http::{Request, StatusCode},
    response::IntoResponse,
};
use leptos::prelude::*;
use leptos_axum::{LeptosRoutes, generate_route_list, render_app_to_stream};
use tower::ServiceExt;
use tower_http::services::ServeDir;

use cowabunga_ui::App;

#[tokio::main]
async fn main() {
    let conf = get_configuration(None).unwrap();
    let leptos_options = conf.leptos_options;
    let addr = leptos_options.site_addr;
    let routes = generate_route_list(App);

    tracing::info!("CowabungaAI UI listening on {}", addr);

    let app = Router::new()
        .leptos_routes(&leptos_options, routes, {
            let leptos_options = leptos_options.clone();
            move || shell(leptos_options.clone())
        })
        .fallback(file_and_error_handler)
        .with_state(leptos_options);

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

fn shell(options: LeptosOptions) -> impl IntoView {
    use leptos_meta::*;
    view! {
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <AutoReload options=options.clone()/>
                <HydrationScripts options/>
                <MetaTags/>
            </head>
            <body>
                <App/>
            </body>
        </html>
    }
}

async fn file_and_error_handler(
    uri: axum::http::Uri,
    State(options): State<LeptosOptions>,
    req: Request<Body>,
) -> impl IntoResponse {
    let root = options.site_root.clone();
    if let Ok(res) = get_static_file(uri.clone(), &root).await {
        if res.status() == StatusCode::OK {
            return res.into_response();
        }
    }
    let handler = render_app_to_stream(move || shell(options.clone()));
    handler(req).await.into_response()
}

async fn get_static_file(
    uri: axum::http::Uri,
    root: &str,
) -> Result<axum::response::Response, (StatusCode, String)> {
    let req = Request::builder().uri(uri).body(Body::empty()).unwrap();
    match ServeDir::new(root).oneshot(req).await {
        Ok(res) => Ok(res.into_response()),
        Err(err) => Err((StatusCode::INTERNAL_SERVER_ERROR, format!("{err}"))),
    }
}
