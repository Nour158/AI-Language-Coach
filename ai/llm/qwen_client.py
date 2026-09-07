import os
import requests


class QwenClient:
    def __init__(self, api_url=None, timeout=180):
        self.api_url = (
            api_url
            or os.getenv("QWEN_API_URL")
            or "https://numerous-porous-impending.ngrok-free.dev"
        ).rstrip("/")

        self.timeout = timeout

    def generate(self, prompt, max_new_tokens=256):
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "prompt": prompt,
                    "max_new_tokens": max_new_tokens,
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            if "response" not in data:
                raise ValueError(
                    "Invalid response from Qwen API: missing 'response'."
                )

            return data["response"].strip()

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                f"Failed to connect to Qwen API: {exc}"
            ) from exc