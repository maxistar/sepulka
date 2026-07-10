import json
import os
import urllib.error
import urllib.request
from pathlib import Path


class LLMError(RuntimeError):
    pass


def load_env(path: str = ".env") -> None:
    """Load a minimal .env file without pulling in a framework.

    Existing environment variables win, which makes deployment and shell usage
    predictable.
    """

    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


class LLMClient:
    """Tiny OpenAI-compatible chat completions client."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        load_env()
        self.base_url = (base_url or os.getenv("LLM_BASE_URL") or "").rstrip("/")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.model = model or os.getenv("LLM_MODEL")

        missing = [name for name, value in {
            "LLM_BASE_URL": self.base_url,
            "LLM_API_KEY": self.api_key,
            "LLM_MODEL": self.model,
        }.items() if not value]
        if missing:
            raise LLMError(f"Missing required LLM settings: {', '.join(missing)}")

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise LLMError(f"LLM HTTP error {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise LLMError(f"LLM connection error: {error.reason}") from error

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as error:
            raise LLMError(f"Unexpected LLM response: {data}") from error
