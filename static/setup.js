const state = {
  credentialsJson: "",
  serviceEmail: "",
};

const els = {
  form: document.querySelector("#setupForm"),
  credentialsFile: document.querySelector("#credentialsFile"),
  credentialsPath: document.querySelector("#credentialsPath"),
  serviceEmail: document.querySelector("#serviceEmail"),
  spreadsheet: document.querySelector("#spreadsheet"),
  projectCurrency: document.querySelector("#projectCurrency"),
  profileName: document.querySelector("#profileName"),
  profileSurname: document.querySelector("#profileSurname"),
  profileEmail: document.querySelector("#profileEmail"),
  submitButton: document.querySelector("#submitButton"),
  status: document.querySelector("#setupStatus"),
  steps: document.querySelector("#setupSteps"),
};

init();

async function init() {
  bindEvents();
  try {
    const status = await fetchJson("/api/setup/status");
    renderStatus(status);
  } catch (error) {
    setStatus(`Unable to load setup status: ${friendlyError(error)}`, "error");
  }
}

function bindEvents() {
  els.credentialsFile.addEventListener("change", readCredentialsFile);
  els.form.addEventListener("submit", submitSetup);
}

function renderStatus(status) {
  const currencies = status.supported_project_currencies || ["EUR"];
  els.projectCurrency.innerHTML = currencies
    .map((currency) => `<option value="${escapeHtml(currency)}">${escapeHtml(currency)}</option>`)
    .join("");
  els.projectCurrency.value = status.project_currency || "EUR";
  els.credentialsPath.value = status.credentials_path || status.default_credentials_path || "credentials/ledger-public-service-account.json";
  els.spreadsheet.value = status.spreadsheet_id || "";

  const profile = status.profile || {};
  els.profileName.value = profile.name || "";
  els.profileSurname.value = profile.surname || "";
  els.profileEmail.value = profile.email || "";

  if (status.service_account_email) {
    state.serviceEmail = status.service_account_email;
    els.serviceEmail.textContent = status.service_account_email;
  }

  els.steps.innerHTML = (status.steps || [])
    .map(
      (step, index) => `
        <li>
          <span>${index + 1}</span>
          <div>
            <strong>${escapeHtml(step.label || "")}</strong>
            <p>${escapeHtml(step.detail || "")}</p>
          </div>
        </li>
      `,
    )
    .join("");

  if (status.complete) {
    setStatus("Google Sheets setup is already complete. Opening Ledger.", "success");
    window.setTimeout(() => {
      window.location.href = "/";
    }, 900);
  }
}

async function readCredentialsFile() {
  const file = els.credentialsFile.files?.[0];
  if (!file) return;
  try {
    const text = await file.text();
    const payload = JSON.parse(text);
    if (payload.type !== "service_account" || !payload.client_email) {
      throw new Error("That JSON file is not a Google service-account key.");
    }
    state.credentialsJson = text;
    state.serviceEmail = payload.client_email;
    els.serviceEmail.textContent = payload.client_email;
    els.credentialsPath.value = "credentials/ledger-public-service-account.json";
    setStatus("Key loaded. Share the Google Sheet with the email shown above.", "");
  } catch (error) {
    state.credentialsJson = "";
    state.serviceEmail = "";
    els.serviceEmail.textContent = "Upload a valid service-account key.";
    setStatus(friendlyError(error), "error");
  }
}

async function submitSetup(event) {
  event.preventDefault();
  setStatus("Checking Google access and creating starter tabs.", "");
  els.submitButton.disabled = true;

  const payload = {
    credentials_json: state.credentialsJson,
    credentials_path: els.credentialsPath.value.trim(),
    spreadsheet: els.spreadsheet.value.trim(),
    project_currency: els.projectCurrency.value,
    name: els.profileName.value.trim(),
    surname: els.profileSurname.value.trim(),
    email: els.profileEmail.value.trim(),
  };

  try {
    const result = await fetchJson("/api/setup/complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values: payload }),
    });
    const seeded = Array.isArray(result.seeded_sheets) && result.seeded_sheets.length
      ? ` Seeded: ${result.seeded_sheets.join(", ")}.`
      : "";
    setStatus(`Setup complete.${seeded} Opening Ledger.`, "success");
    window.setTimeout(() => {
      window.location.href = "/";
    }, 1200);
  } catch (error) {
    setStatus(friendlyError(error), "error");
    els.submitButton.disabled = false;
  }
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = { error: text };
  }
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || response.statusText || "Request failed.");
  }
  return payload;
}

function setStatus(message, type) {
  els.status.textContent = message || "";
  els.status.classList.toggle("is-error", type === "error");
  els.status.classList.toggle("is-success", type === "success");
}

function friendlyError(error) {
  return error instanceof Error ? error.message : String(error || "Unexpected setup error.");
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
