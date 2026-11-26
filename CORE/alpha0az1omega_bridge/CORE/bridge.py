"""Local FastAPI bridge between the Alpha0az1omega UI and Ollama.

Run from the project root with:
    python3 -m uvicorn CORE.bridge:app --host 127.0.0.1 --port 8000

The server binds to loopback only and never exposes Ollama to the network.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3.8:27b"
ALLOWED_MODELS = {
    "qwen3.8:27b",
    "deepseek-r1:8b",
    "qwen2.5:7b",
    "gemma3:4b",
    "llama3.2:3b",
    "llama3.2:1b",
    "aricom-base:latest",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
VISUAL_INDEX = PROJECT_ROOT / "VISUAL" / "index.html"

app = FastAPI(
    title="Alpha0az1omega Local Bridge",
    version="0.1.0",
    description="Loopback-only bridge from the local UI to the local Ollama API.",
)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=12000)
    model: str = DEFAULT_MODEL


class ChatResponse(BaseModel):
    model: str
    response: str
    done: bool


def _ollama_json(path: str, payload: dict | None = None, timeout: int = 240) -> dict:
    url = f"{OLLAMA_BASE_URL}{path}"
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method="GET" if data is None else "POST")

    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:1000]
        raise HTTPException(status_code=502, detail=f"Ollama HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Ollama local is unreachable. Check that Ollama is running on this Mac.",
        ) from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=502, detail="Ollama returned invalid JSON.") from exc


@app.get("/api/health")
def health() -> dict:
    """Report whether Ollama responds and list the model names it exposes."""
    data = _ollama_json("/api/tags", timeout=8)
    models = [item.get("name", "") for item in data.get("models", []) if item.get("name")]
    return {"status": "ok", "ollama": "connected", "models": models}


@app.post("/api/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    """Send one user prompt to an allow-listed local Ollama model."""
    if body.model not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail="Model is not in the local allow-list.")

    result = _ollama_json(
        "/api/chat",
        {
            "model": body.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Nexus, the local AI assistant of Alpha0az1omega. "
                        "Be clear, precise, and honest about uncertainty. "
                        "Do not claim that a statement has been formally verified "
                        "unless a verifier has actually checked it."
                    ),
                },
                {"role": "user", "content": body.prompt},
            ],
            "stream": False,
        },
        timeout=240,
    )

    message = result.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(status_code=502, detail="Ollama returned no assistant message.")

    return ChatResponse(model=body.model, response=content, done=bool(result.get("done", False)))


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the existing V19 page locally without rewriting it."""
    if not VISUAL_INDEX.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"VISUAL/index.html not found at {VISUAL_INDEX}. Put this file in CORE/.",
        )
    return FileResponse(VISUAL_INDEX)
