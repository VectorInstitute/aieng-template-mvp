/* ── DOM refs ─────────────────────────────────────────────── */
const promptInput    = document.getElementById("prompt-input");
const charCountEl    = document.getElementById("char-count");
const submitBtn      = document.getElementById("submit-btn");
const resultSection  = document.getElementById("result-section");
const loadingState   = document.getElementById("loading-state");
const loadingMsg     = document.getElementById("loading-msg");
const outputContainer = document.getElementById("output-container");
const outputText     = document.getElementById("output-text");
const errorBannerEl  = document.getElementById("error-banner");

/* ── Config ───────────────────────────────────────────────── */
const MAX_CHARS           = 2000;
const MAX_COLD_START_RETRIES = 10;
let coldStartRetries      = 0;

/* ── Helpers ──────────────────────────────────────────────── */
function showError(msg) {
  errorBannerEl.textContent = msg;
  errorBannerEl.classList.remove("hidden");
}

function hideError() {
  errorBannerEl.classList.add("hidden");
  errorBannerEl.textContent = "";
}

function setLoading(active, msg = "Generating…") {
  resultSection.classList.toggle("hidden", !active && outputText.textContent === "");
  loadingState.classList.toggle("hidden", !active);
  loadingMsg.textContent = msg;
  submitBtn.disabled = active;
}

/* ── Char counter ─────────────────────────────────────────── */
promptInput.addEventListener("input", () => {
  charCountEl.textContent = promptInput.value.length;
});

/* ── Submit ───────────────────────────────────────────────── */
submitBtn.addEventListener("click", () => {
  const prompt = promptInput.value.trim();
  if (!prompt) return;
  hideError();
  coldStartRetries = 0;
  runGenerate(prompt);
});

async function runGenerate(prompt) {
  setLoading(true);
  outputContainer.classList.add("hidden");
  outputText.textContent = "";
  resultSection.classList.remove("hidden");

  const started = Date.now();

  try {
    await streamGenerate(prompt);
    coldStartRetries = 0;
    submitBtn.disabled = false;

    const elapsed = (Date.now() - started) / 1000;
    if (elapsed > 8) {
      showError(`Note: the GPU service was cold — first request took ${elapsed.toFixed(0)}s to load.`);
    }
  } catch (err) {
    const status = err && err.status;
    if (status === 429) {
      setLoading(false);
      showError("Rate limit reached — please wait a moment before trying again.");
    } else if ((status === 502 || status === 503) && coldStartRetries < MAX_COLD_START_RETRIES) {
      coldStartRetries++;
      let secs = 5;
      const countdown = setInterval(() => {
        secs--;
        if (secs > 0) {
          setLoading(true, `Server loading — retrying in ${secs}s… (attempt ${coldStartRetries}/${MAX_COLD_START_RETRIES})`);
        } else {
          clearInterval(countdown);
          runGenerate(prompt);
        }
      }, 1000);
      setLoading(true, `Server loading — retrying in ${secs}s… (attempt ${coldStartRetries}/${MAX_COLD_START_RETRIES})`);
    } else {
      setLoading(false);
      showError(`Generation failed: ${err.message || "Unknown error"}`);
    }
  }
}

async function streamGenerate(prompt) {
  const res = await fetch("/generate/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  if (!res.ok) {
    const httpErr = new Error(`Server error (${res.status})`);
    httpErr.status = res.status;
    throw httpErr;
  }

  outputContainer.classList.remove("hidden");
  loadingState.classList.add("hidden");  // hide spinner; button stays disabled until stream ends

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });

    const lines = buf.split("\n");
    buf = lines.pop(); // keep incomplete line

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      try {
        const data = JSON.parse(line.slice(6));
        if (data.error) {
          const e = new Error(data.error);
          throw e;
        }
        if (data.done) return;
        if (data.t) {
          outputText.textContent += data.t;
        }
      } catch (parseErr) {
        throw parseErr;
      }
    }
  }
}
