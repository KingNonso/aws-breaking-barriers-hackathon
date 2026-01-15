// Configuration for environment-specific API endpoints
const CONFIG = {
  // API Gateway REST endpoint
  API_BASE_URL: process.env.API_BASE_URL || "https://api.example.com/prod",

  // WebSocket API endpoint
  WEBSOCKET_URL: process.env.WEBSOCKET_URL || "wss://ws.example.com/prod",

  // Environment
  ENVIRONMENT: process.env.ENVIRONMENT || "development",

  // Session timeout (1 hour in milliseconds)
  SESSION_TIMEOUT: 60 * 60 * 1000,

  // WebSocket reconnection settings
  WS_MAX_RECONNECT_ATTEMPTS: 5,
  WS_RECONNECT_BASE_DELAY: 1000,
  WS_RECONNECT_MAX_DELAY: 30000,

  // Polling fallback interval (2 seconds)
  POLLING_INTERVAL: 2000,

  // Auto-navigation delays
  SCREEN_TRANSITION_DELAY: 2000,
  RISK_ASSESSMENT_DELAY: 3000,
};

// Environment-specific overrides
if (typeof window !== "undefined") {
  // Check for environment variables in window object (set by build process)
  if (window.ENV_API_BASE_URL) {
    CONFIG.API_BASE_URL = window.ENV_API_BASE_URL;
  }
  if (window.ENV_WEBSOCKET_URL) {
    CONFIG.WEBSOCKET_URL = window.ENV_WEBSOCKET_URL;
  }
  if (window.ENV_ENVIRONMENT) {
    CONFIG.ENVIRONMENT = window.ENV_ENVIRONMENT;
  }
}

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = CONFIG;
}
