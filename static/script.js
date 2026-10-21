
const form = document.getElementById("prediction-form");
const featureGrid = document.getElementById("feature-grid");
const button = document.getElementById("analyze-button");
const errorBox = document.getElementById("form-error");

let analysisCount = 0;
let transactionNumber = 0;

const sessionHistory = [];

const money = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2
  }).format(value);

function addFeatureInputs() {
  for (let i = 1; i <= 28; i++) {
    const label = document.createElement("label");
    label.textContent = `V${i}`;

    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.value = "0";
    input.id = `v${i}`;
    input.name = `V${i}`;
    input.setAttribute("aria-label", `Feature V${i}`);

    label.appendChild(input);
    featureGrid.appendChild(label);
  }
}

function setModelStatus(ready, message) {
  document.getElementById("model-status").textContent = message;
  document.getElementById("metric-model").textContent =
    ready ? "Online" : "Offline";
  document.getElementById("metric-model-note").textContent = message;
}

async function checkModel() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();

    setModelStatus(
      response.ok && data.model_loaded,
      response.ok && data.model_loaded
        ? "Model loaded successfully"
        : "Model not loaded"
    );
  } catch {
    setModelStatus(false, "Flask connection unavailable");
  }
}

function showError(message) {
  errorBox.textContent = message;
}

function clearError() {
  errorBox.textContent = "";
}

function updateResult(data, enteredMinutes) {
  const isFraud = Number(data.prediction) === 1;
  const risk = Math.max(0, Math.min(100, Number(data.risk_score)));

  document.getElementById("empty-result").hidden = true;
  document.getElementById("result-content").hidden = false;

  const ring = document.getElementById("risk-ring");
  const degrees = risk * 3.6;
  const riskColor = isFraud ? "#ff414d" : "#ff8a24";

  ring.style.background = `conic-gradient(
    ${riskColor} ${degrees}deg,
    #442525 ${degrees}deg
  )`;

  document.getElementById("risk-number").textContent =
    `${risk.toFixed(2)}%`;

  const status = document.getElementById("result-status");
  status.textContent = data.label;
  status.classList.toggle("high", isFraud);

  document.getElementById("result-description").textContent = isFraud
    ? "The model classified this transaction as potentially fraudulent. Investigate before taking action."
    : "The model classified this transaction as likely legitimate. This does not guarantee that it is safe.";

  document.getElementById("result-amount").textContent = money(data.amount);
  document.getElementById("result-time").textContent =
    `${enteredMinutes} min (${Number(data.model_time_seconds).toFixed(2)} sec)`;

  document.getElementById("result-prediction").textContent =
    isFraud ? "Class 1 · Fraud" : "Class 0 · Legitimate";

  document.getElementById("metric-risk").textContent =
    `${risk.toFixed(2)}%`;

  document.getElementById("metric-amount").textContent = money(data.amount);

  analysisCount++;
  transactionNumber++;

  document.getElementById("metric-count").textContent = analysisCount;

  sessionHistory.unshift({
    id: `FS-${String(transactionNumber).padStart(4, "0")}`,
    amount: data.amount,
    minutes: enteredMinutes,
    risk,
    label: data.label,
    isFraud,
    time: new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit"
    })
  });

  renderHistory();
}

function renderHistory() {
  const tbody = document.getElementById("activity-body");
  tbody.replaceChildren();

  if (sessionHistory.length === 0) {
    const row = tbody.insertRow();
    row.className = "empty-row";
    const cell = row.insertCell();
    cell.colSpan = 5;
    cell.textContent = "No transactions analyzed yet.";
    return;
  }

  sessionHistory.slice(0, 10).forEach((item) => {
    const row = tbody.insertRow();

    row.insertCell().textContent = item.id;
    row.insertCell().textContent = money(item.amount);
    row.insertCell().textContent = `${item.minutes} min`;
    row.insertCell().textContent = `${item.risk.toFixed(2)}%`;

    const statusCell = row.insertCell();
    const pill = document.createElement("span");

    pill.className = `table-pill${item.isFraud ? " high" : ""}`;
    pill.textContent = item.label;

    statusCell.appendChild(pill);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();

  const amount = Number(document.getElementById("amount").value);
  const timeMinutes = Number(document.getElementById("time").value);

  if (!Number.isFinite(amount) || amount < 0) {
    showError("Enter a valid non-negative transaction amount.");
    return;
  }

  if (!Number.isFinite(timeMinutes) || timeMinutes < 0) {
    showError("Enter a valid non-negative time in minutes.");
    return;
  }

  // Convert the user's minutes to seconds for the model.
  const timeSeconds = timeMinutes * 60;

  if (!Number.isFinite(timeSeconds)) {
    showError("Time value is too large.");
    return;
  }

  const payload = {
    Time: timeSeconds,
    Amount: amount
  };

  for (let i = 1; i <= 28; i++) {
    const value = Number(document.getElementById(`v${i}`).value);

    if (!Number.isFinite(value)) {
      showError(`Enter a valid numeric value for V${i}.`);
      return;
    }

    payload[`V${i}`] = value;
  }

  button.disabled = true;
  button.querySelector("span:first-child").textContent =
    "Analyzing transaction…";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Prediction request failed.");
    }

    // Preserve the user's original minutes for display.
    updateResult(data, timeMinutes);
  } catch (error) {
    showError(
      error.message || "Unable to connect to the prediction service."
    );
  } finally {
    button.disabled = false;
    button.querySelector("span:first-child").textContent =
      "Run fraud analysis";
  }
});

addFeatureInputs();
checkModel();
renderHistory();
