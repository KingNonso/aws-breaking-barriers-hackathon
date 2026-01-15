// API Client module for REST API communication
class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async submitIncident(indicatorType, indicatorValue, source) {
    const response = await fetch(`${this.baseURL}/incidents`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        indicator_type: indicatorType,
        indicator_value: indicatorValue,
        source: source || "web_ui",
        metadata: {
          user_agent: navigator.userAgent,
          timestamp: new Date().toISOString(),
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }

  async getIncidentStatus(incidentId) {
    const response = await fetch(`${this.baseURL}/incidents/${incidentId}`);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  }

  async downloadBrief(incidentId) {
    const response = await fetch(
      `${this.baseURL}/incidents/${incidentId}/brief`
    );

    if (!response.ok) {
      throw new Error(`Failed to generate brief`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `case-brief-${incidentId}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }
}

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = APIClient;
}
