const API_BASE_URL = "http://localhost:8000";

async function parseResponse(response) {
  if (!response.ok) {
    let message = "Request failed.";
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Keep fallback message.
    }
    throw new Error(message);
  }

  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return parseResponse(response);
}

export async function sendMessage(
  sessionId,
  message,
  history,
  inputType = "text"
){
  const response = await fetch(
    `${API_BASE_URL}/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
       session_id: sessionId,
       message,
      history,
      input_type: inputType,
    }),
    }
  );

  return parseResponse(response);
}

export async function evaluateSession(history) {
  const response = await fetch(`${API_BASE_URL}/session/evaluate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ history }),
  });

  return parseResponse(response);
}

export async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "recording.webm");

  const response = await fetch(`${API_BASE_URL}/voice/transcribe`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}
