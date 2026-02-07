import json
from typing import Any, Dict, Optional

from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from config import GROQ_API_KEY, GROQ_MODEL


class GroqClient:
    """
    Thin wrapper around Groq chat completions.

    - Centralizes model/temperature selection
    - Provides a helper for JSON-style outputs with basic robustness
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        if not api_key and not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Set it in your environment to use LLM features."
            )

        self._client = Groq(api_key=api_key or GROQ_API_KEY)
        self._model = model or GROQ_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """Generic chat completion that returns raw text."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """
        Chat completion that is expected to return JSON.

        The prompt MUST clearly instruct the model to emit ONLY a JSON object.
        This helper then best-effort parses the response into a dict.
        """
        response_text = self.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Fast path: direct JSON
        try:
            return json.loads(response_text)
        except Exception:
            pass

        # Fallback: strip code fences if present
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            # Remove possible language hint like ```json
            first_newline = cleaned.find("\n")
            if first_newline != -1:
                cleaned = cleaned[first_newline + 1 :]

        try:
            return json.loads(cleaned)
        except Exception:
            # As an ultimate fallback, wrap raw text
            return {"_raw": response_text}


_groq_client: Optional[GroqClient] = None


def get_groq_client() -> GroqClient:
    """Singleton-style accessor to avoid re-initializing the SDK repeatedly."""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client

