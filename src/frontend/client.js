// -------------------------
// LOGGER
// -------------------------
const log = (msg) => {
  const el = document.getElementById('log');
  if (!el) return;

  el.textContent += msg + '\n';
  el.scrollTop = el.scrollHeight;
};

// -------------------------
// WEBSOCKET SETUP
// -------------------------
const WS_URL = "ws://localhost:8000/ws/audio";
const SESSION_ID = "patient_456";

const ws = new WebSocket(WS_URL);

// -------------------------
// ON OPEN
// -------------------------
ws.onopen = () => {
  log("WebSocket connected");

  ws.send(JSON.stringify({
    type: "start_session",
    session_id: SESSION_ID
  }));
};

// -------------------------
// ON MESSAGE
// -------------------------
ws.onmessage = async (event) => {
  try {
    const msg = JSON.parse(event.data);

    // -------------------------
    // SESSION STARTED
    // -------------------------
    if (msg.event === "session_started") {
      log("Session started: " + msg.session_id);
      return;
    }

    // -------------------------
    // RESPONSE META (LATENCY)
    // -------------------------
    if (msg.event === "response_meta") {
      const latency = msg.meta && msg.meta.latency_ms
        ? msg.meta.latency_ms
        : 0;

      log("Latency: " + latency.toFixed(1) + " ms");
      return;
    }

    // -------------------------
    // AUDIO RESPONSE
    // -------------------------
    if (msg.event === "audio_base64") {
      log("Playing audio response...");

      // Convert base64 → binary
      const binary = atob(msg.data);
      const bytes = new Uint8Array(binary.length);

      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }

      // Create audio blob
      const blob = new Blob([bytes], { type: "audio/mp3" });
      const url = URL.createObjectURL(blob);

      const audio = new Audio(url);
      audio.play();

      return;
    }

    // -------------------------
    // UNKNOWN EVENT
    // -------------------------
    log("Message: " + JSON.stringify(msg));

  } catch (err) {
    log("Error parsing message");
    console.error(err);
  }
};

// -------------------------
// ERROR HANDLING
// -------------------------
ws.onerror = (err) => {
  log("WebSocket error");
  console.error(err);
};

ws.onclose = () => {
  log("WebSocket closed");
};

// -------------------------
// TEST BUTTON
// -------------------------
document.getElementById("test").addEventListener("click", () => {
  const transcript = prompt(
    "Enter your message",
    "Book appointment tomorrow"
  );

  if (!transcript) return;

  ws.send(JSON.stringify({
    type: "speech_end",
    transcript: transcript,
    lang: "en",
    session_id: SESSION_ID
  }));

  log("You: " + transcript);
});