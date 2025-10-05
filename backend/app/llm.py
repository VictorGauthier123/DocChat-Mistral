import os
import httpx


class MistralClient:
    def __init__(self, model: str = "mistral-small-latest"):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ MISTRAL_API_KEY non défini dans l'environnement")
        self.model = model

    def generate(self, prompt: str) -> str:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        with httpx.Client(timeout=60) as client:
            r = client.post(url, headers=headers, json=body)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
