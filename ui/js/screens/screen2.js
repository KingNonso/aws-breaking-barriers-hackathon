// Screen 2: Real-Time Analysis Logic
(function () {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const wsManager = new WebSocketManager(CONFIG.WEBSOCKET_URL);

  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  const logContainer = document.getElementById("live-log");
  const contextPanel = document.getElementById("investigation-context");
  const networkGraph = document.getElementById("network-graph");

  let pollingInterval = null;
  let analysisComplete = false;

  async function init() {
    if (!incidentId) {
      window.location.href = "/screen1";
      return;
    }

    try {
      await wsManager.connect(incidentId);
      setupWebSocketListeners();
    } catch (error) {
      console.error("WebSocket failed, using polling fallback", error);
      startPolling();
    }
  }

  function setupWebSocketListeners() {
    wsManager.on("agent_phase", (data) => {
      updateLog(data.phase, data.status, data.message);

      if (data.phase === "observe" && data.status === "complete") {
        analysisComplete = true;
        setTimeout(
          () =>
            (window.location.href = `/screen3?incident_id=${incidentId}`),
          CONFIG.SCREEN_TRANSITION_DELAY
        );
      }
    });

    wsManager.on("context_update", (data) => {
      if (contextPanel) updateContext(data);
    });

    wsManager.on("network_update", (data) => {
      if (networkGraph) updateNetwork(data);
    });
  }

  function startPolling() {
    pollingInterval = setInterval(async () => {
      try {
        const status = await apiClient.getIncidentStatus(incidentId);
        if (status.status === "complete") {
          clearInterval(pollingInterval);
          window.location.href = `/screen3?incident_id=${incidentId}`;
        }
      } catch (error) {
        console.error("Polling error:", error);
      }
    }, CONFIG.POLLING_INTERVAL);
  }

  function updateLog(phase, status, message) {
    if (!logContainer) return;

    const entry = document.createElement("div");
    entry.className = "log-entry p-2 border-b border-gray-200";
    entry.innerHTML = `
      <span class="font-mono text-xs text-gray-500">${new Date().toLocaleTimeString()}</span>
      <span class="font-semibold">[${phase.toUpperCase()}]</span>
      <span class="${status === "complete" ? "text-green-600" : "text-blue-600"}">${status}</span>
      <p class="text-sm mt-1">${message}</p>
    `;
    logContainer.appendChild(entry);
    logContainer.scrollTop = logContainer.scrollHeight;
  }

  function updateContext(data) {
    contextPanel.innerHTML = `
      <div class="p-4">
        <h3 class="font-semibold mb-2">Historical Data</h3>
        <p class="text-sm">Cases found: ${data.cases_found || 0}</p>
        <p class="text-sm">Patterns identified: ${data.patterns || 0}</p>
      </div>
    `;
  }

  function updateNetwork(data) {
    networkGraph.innerHTML = `
      <div class="p-4">
        <p class="text-sm">Connected entities: ${data.connections || 0}</p>
      </div>
    `;
  }

  init();
})();
