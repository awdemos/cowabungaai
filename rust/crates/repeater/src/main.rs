//! CowabungaAI repeater backend binary.

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| "info".into()),
        )
        .init();

    let addr = std::env::var("REPEATER_BIND")
        .unwrap_or_else(|_| "0.0.0.0:50051".to_string())
        .parse()?;
    tracing::info!(%addr, "cowabunga-repeater listening");

    cowabunga_repeater::serve(addr).await?;

    Ok(())
}
