// Screen 3: Risk Assessment Logic
(function () {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);

  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  const riskScoreEl = document.getElementById("risk-score");
  const classificationEl = document.getElementById("classification");
  const reasoningEl = document.getElementById("ai-reasoning");
  const networkVizEl = document.getElementById("network-viz");

  async function init() {
    if (!incidentId) {
      window.location.href = "/screen1";
      return;
    }

    try {
      const data = await apiClient.getIncidentStatus(incidentId);
      displayRiskAssessment(data);

      setTimeout(
        () => (window.location.href = `/screen4?incident_id=${incidentId}`),
        CONFIG.RISK_ASSESSMENT_DELAY
      );
    } catch (error) {
      console.error("Failed to load risk assessment:", error);
    }
  }

  function displayRiskAssessment(data) {
    const risk = data.risk_assessment || {};

    if (riskScoreEl) {
      riskScoreEl.textContent = risk.score || 0;
      riskScoreEl.className = getRiskClass(risk.score);
    }

    if (classificationEl) {
      classificationEl.textContent = risk.classification || "UNKNOWN";
      classificationEl.className = getClassificationClass(risk.classification);
    }

    if (reasoningEl) {
      const factors = risk.factors || [];
      reasoningEl.innerHTML = factors
        .map((f) => `<li class="mb-2">${f}</li>`)
        .join("");
    }

    if (networkVizEl && data.pattern_analysis) {
      networkVizEl.innerHTML = `
        <div class="p-4">
          <p class="text-sm">Linked cases: ${data.pattern_analysis.linked_cases || 0}</p>
          <p class="text-sm">Network size: ${data.pattern_analysis.network_size || 0}</p>
        </div>
      `;
    }
  }

  function getRiskClass(score) {
    if (score >= 80) return "text-red-600 font-bold text-4xl";
    if (score >= 50) return "text-orange-600 font-bold text-4xl";
    return "text-yellow-600 font-bold text-4xl";
  }

  function getClassificationClass(classification) {
    const classes = {
      CRITICAL: "bg-red-600 text-white px-4 py-2 rounded",
      PRIORITY: "bg-orange-600 text-white px-4 py-2 rounded",
      MONITOR: "bg-yellow-600 text-white px-4 py-2 rounded",
    };
    return classes[classification] || "bg-gray-600 text-white px-4 py-2 rounded";
  }

  init();
})();
