// Screen 5: Impact Summary Logic
(function () {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const sessionManager = new SessionManager();

  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  const processingTimeEl = document.getElementById("processing-time");
  const casesSearchedEl = document.getElementById("cases-searched");
  const victimsIdentifiedEl = document.getElementById("victims-identified");
  const threatLevelEl = document.getElementById("threat-level");
  const agenciesAlertedEl = document.getElementById("agencies-alerted");
  const downloadBtn = document.getElementById("download-brief-btn");

  async function init() {
    if (!incidentId) {
      window.location.href = "/screen1";
      return;
    }

    try {
      const data = await apiClient.getIncidentStatus(incidentId);
      displaySummary(data);
    } catch (error) {
      console.error("Failed to load summary:", error);
    }

    if (downloadBtn) {
      downloadBtn.addEventListener("click", async () => {
        try {
          await apiClient.downloadBrief(incidentId);
        } catch (error) {
          alert("Failed to download brief: " + error.message);
        }
      });
    }

    // Clear session after viewing summary
    setTimeout(() => sessionManager.clearSession(), 5000);
  }

  function displaySummary(data) {
    const startTime = new Date(data.created_at || Date.now());
    const endTime = new Date(data.completed_at || Date.now());
    const processingTime = Math.round((endTime - startTime) / 1000);

    if (processingTimeEl) {
      processingTimeEl.textContent = `${processingTime}s`;
    }

    if (casesSearchedEl) {
      casesSearchedEl.textContent =
        data.pattern_analysis?.cases_searched || "0";
    }

    if (victimsIdentifiedEl) {
      victimsIdentifiedEl.textContent =
        data.pattern_analysis?.victims_identified || "0";
    }

    if (threatLevelEl) {
      const level = data.risk_assessment?.classification || "UNKNOWN";
      threatLevelEl.textContent = level;
      threatLevelEl.className = getThreatClass(level);
    }

    if (agenciesAlertedEl) {
      agenciesAlertedEl.textContent =
        data.alert_dispatch?.agencies?.length || "0";
    }
  }

  function getThreatClass(level) {
    const classes = {
      CRITICAL: "text-red-600 font-bold",
      PRIORITY: "text-orange-600 font-bold",
      MONITOR: "text-yellow-600 font-bold",
    };
    return classes[level] || "text-gray-600 font-bold";
  }

  init();
})();
