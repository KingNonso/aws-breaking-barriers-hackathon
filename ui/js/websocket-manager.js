// WebSocket Manager module for real-time updates
class WebSocketManager {
  constructor(wsURL) {
    this.wsURL = wsURL;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.listeners = {};
  }

  connect(incidentId) {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(`${this.wsURL}?incident_id=${incidentId}`);

      this.ws.onopen = () => {
        console.log("WebSocket connected");
        this.reconnectAttempts = 0;
        resolve();
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        reject(error);
      };

      this.ws.onclose = () => {
        console.log("WebSocket closed");
        this.attemptReconnect(incidentId);
      };
    });
  }

  handleMessage(data) {
    const { type, payload } = data;

    if (this.listeners[type]) {
      this.listeners[type].forEach((callback) => callback(payload));
    }
  }

  on(eventType, callback) {
    if (!this.listeners[eventType]) {
      this.listeners[eventType] = [];
    }
    this.listeners[eventType].push(callback);
  }

  attemptReconnect(incidentId) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(
        `Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`
      );
      setTimeout(() => this.connect(incidentId), delay);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = WebSocketManager;
}
