// Screen 4: Alert Dispatch Logic
(function () {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);

  const urlParams = new URLSearchParams(window.location.search);
  const incidentId = urlParams.get("incident_id");

  const agencyListEl = document.getElementById("agency-list");
  const viewBriefBtn = document.getElementById("view-brief-btn");

  async function init() {
    if (!incidentId) {
      window.location.href = "/screen1";
      return;
    }

    try {
      const data = await apiClient.getIncidentStatus(incidentId);
      displayAlertDispatch(data);
    } catch (error) {
      console.error("Failed to load alert dispatch:", error);
    }

    if (viewBriefBtn) {
      viewBriefBtn.addEventListener("click", () => {
        window.location.href = `/screen5?incident_id=${incidentId}`;
      });
    }
  }

  function displayAlertDispatch(data) {
    const alerts = data.alert_dispatch || {};
    const agencies = alerts.agencies || [];

    if (agencyListEl) {
      agencyListEl.innerHTML = agencies
        .map(
          (agency) => `
        <div class="agency-card p-4 border rounded mb-2">
          <h4 class="font-semibold">${agency.name}</h4>
          <div class="flex gap-4 mt-2">
            <span class="status-indicator ${agency.sms_sent ? "text-green-600" : "text-gray-400"}">
              📱 SMS ${agency.sms_sent ? "✓" : "⏳"}
            </span>
            <span class="status-indicator ${agency.email_sent ? "text-green-600" : "text-gray-400"}">
              📧 Email ${agency.email_sent ? "✓" : "⏳"}
            </span>
          </div>
        </div>
      `
        )
        .join("");

      // Simulate delivery confirmations
      setTimeout(() => animateDelivery(), 1000);
    }
  }

  function animateDelivery() {
    const indicators = document.querySelectorAll(".status-indicator");
    indicators.forEach((el, idx) => {
      setTimeout(() => {
        el.classList.remove("text-gray-400");
        el.classList.add("text-green-600");
        el.textContent = el.textContent.replace("⏳", "✓");
      }, idx * 500);
    });
  }

  init();
})();
