// Screen 1: Data Input Logic
(function () {
  const apiClient = new APIClient(CONFIG.API_BASE_URL);
  const sessionManager = new SessionManager();

  const form = document.getElementById("incident-form");
  const submitBtn = document.getElementById("submit-btn");
  const errorMsg = document.getElementById("error-message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const indicatorType = document.getElementById("indicator-type").value;
    const indicatorValue = document.getElementById("indicator-value").value;
    const source = document.getElementById("source").value;

    if (!validateInput(indicatorType, indicatorValue)) {
      showError("Invalid input. Please check your data.");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";

    try {
      const response = await apiClient.submitIncident(
        indicatorType,
        indicatorValue,
        source
      );
      sessionManager.saveSession(response.incident_id, "screen2");
      window.location.href = `/screen2?incident_id=${response.incident_id}`;
    } catch (error) {
      showError(`Submission failed: ${error.message}`);
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit Incident";
    }
  });

  function validateInput(type, value) {
    if (!value || value.trim().length === 0) return false;

    if (type === "phone") {
      return /^[\d\s\-\+\(\)]+$/.test(value);
    } else if (type === "name") {
      return value.length >= 2;
    } else if (type === "transaction_id") {
      return value.length >= 5;
    }
    return true;
  }

  function showError(message) {
    if (errorMsg) {
      errorMsg.textContent = message;
      errorMsg.classList.remove("hidden");
      setTimeout(() => errorMsg.classList.add("hidden"), 5000);
    } else {
      alert(message);
    }
  }
})();
