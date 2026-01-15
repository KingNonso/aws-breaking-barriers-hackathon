// Session Manager module for state persistence
class SessionManager {
  constructor() {
    this.SESSION_KEY = "trafficking_alert_session";
    this.SESSION_TIMEOUT = 60 * 60 * 1000; // 1 hour
  }

  saveSession(incidentId, currentScreen) {
    const session = {
      incident_id: incidentId,
      current_screen: currentScreen,
      timestamp: Date.now(),
    };
    localStorage.setItem(this.SESSION_KEY, JSON.stringify(session));
  }

  getSession() {
    const sessionData = localStorage.getItem(this.SESSION_KEY);
    if (!sessionData) return null;

    const session = JSON.parse(sessionData);
    const age = Date.now() - session.timestamp;

    if (age > this.SESSION_TIMEOUT) {
      this.clearSession();
      return null;
    }

    return session;
  }

  clearSession() {
    localStorage.removeItem(this.SESSION_KEY);
  }

  isSessionActive() {
    return this.getSession() !== null;
  }
}

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = SessionManager;
}
