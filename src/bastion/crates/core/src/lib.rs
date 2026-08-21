src/bastion/crates/core/src/lib.rs

// ============================================================================
// BASTION CORE - CRATES/CORE/MAIN MODULES (Extended & Enhanced)
// ============================================================================

/// A generic HTTP client that handles arbitrary URI formats, including special characters and encoded payloads.
pub mod http_client; // Ensures strict typing on all requests without type erasure during execution.

#[cfg(feature = "http")]
mod http_server {
    use super::*;

    #[derive(Debug)]
    pub struct HttpServerConfig {
        /// The protocol to serve (e.g., HTTP/1.0, HTTPS). Defaults to HTTP/2 if enabled or a specific one is provided.
        pub protocol: Option<String>,
        
        /// Port for the server. If not specified, defaults to 8080 but can be overridden via environment variables.
        #[cfg(feature = "http")]
        pub port: u16,

        /// Maximum request size in bytes (default is very high). Can be set per-request or globally if enabled with `max_size`.
        #[cfg(feature = "http")]
        pub max_request_size: usize, // Default to 4 * 1024 * 1024 for performance reasons.

        /// Enable compression of response headers and body (default is true). Can be disabled via a flag or per-request config if desired.
        #[cfg(feature = "http")]
        pub enable_compression: bool, // Default to false unless explicitly enabled in the request context.
    }

    impl HttpServerConfig {
        /// Create an HTTP server configuration with specific protocol settings and defaults for ports/size.
        pub fn new(protocol_str: Option<String>, port: u16 = 8080) -> Self {
            let config = Self::default();
            
            if !protocol_str.is_empty() && protocol_str != "http" {
                // If a specific custom protocol is requested, use it. Otherwise, default to HTTP/2 for better performance and security (HTTP/1.1 is deprecated).
                config.protocol = Some(protocol_str);
            } else {
                config.protocol = if port > 0 && !protocol_str.is_empty() {
                    // Default behavior: Use the specified protocol or HTTP/2 as a fallback depending on context, but prioritize explicit protocols over defaults for security and performance.
                    None
                } else {
                    Some("http".to_string())
                };

                config.port = port;

                if let Some(max_size) = request_config::get_max_request_size() {
                    // If a max size is configured, use it (or default to 4MB).
                    config.max_request_size = match &max_size {
                        Ok(size) => *size,
                        Err(_) => 4_194_568_u32, // Default high for performance.
                    };

                } else if !protocol_str.is_empty() {
                    config.max_request_size = request_config::get_max_request_size(); // Use the configured max size or default to 4MB if not specified.
                }

                config.enable_compression = true; // Enable compression by default unless disabled in a specific context.
            }
            
            config
        }
    }

    #[derive(Debug)]
    pub struct HttpServer {
        /// The protocol being served (HTTP/1.x, HTTP/2). Defaults to "http".
        pub protocol: Option<String>,
        
        /// Port for the server. If not specified, defaults to 8080 but can be overridden via environment variables.
        #[cfg(feature = "http")]
        pub port: u16,

        /// Maximum request size in bytes (default is very high). Can be set per-request or globally if enabled with `max_size`.
        #[cfg(feature = "http")]
        pub max_request_size: usize, // Default to 4 * 1024 * 1024 for performance reasons.

        /// Enable compression of response headers and body (default is true). Can be disabled via a flag or per-request config if desired.
        #[cfg(feature = "http")]
        pub enable_compression: bool, // Default to false unless explicitly enabled in the request context.
    }

    impl HttpServer {
        /// Create an HTTP server configuration with specific protocol settings and defaults for ports/size.
        fn new(protocol_str: Option<String>, port: u16 = 8080) -> Self {
            let config = Self::default();
            
            if !protocol_str.is_empty() && protocol_str != "http" {
                // If a specific custom protocol is requested, use it. Otherwise, default to HTTP/2 for better performance and security (HTTP/1.1
