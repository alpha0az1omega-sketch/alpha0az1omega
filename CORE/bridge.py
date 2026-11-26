"""
ALPHA0AZ1OMEGA — Main Bridge
FastAPI + Ollama + Z3 + PGP + Epistemic + Creation Studio
"""
import json
import time
import re
import httpx
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from CORE.neuro_symbolic.verifier import verify_response_claims
from CORE.pgp.signer import sign_response, get_chain_summary
from CORE.epistemic.engine import compute_epistemic_score
from CORE.studio.engine import CreationStudio, NodeType

# ─── Configuration ───
DEFAULT_MODEL = "qwen2.5:7b"
OLLAMA_BASE = "http://127.0.0.1:11434"
REQUEST_TIMEOUT = 300.0

# ─── FastAPI App ───
app = FastAPI(title="ALPHA0AZ1OMEGA", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global Creation Studio ───
studio = CreationStudio(operator_id="alpha0az1omega")


# ─── Models ───
class ChatRequest(BaseModel):
    model: str = DEFAULT_MODEL
    prompt: str
    system: str = ""
    num_predict: int = 512
    temperature: float = 0.7
    stream: bool = False


class ChatResponse(BaseModel):
    model: str
    response: str
    done: bool
    verification: dict
    epistemic: dict | None = None
    pgp_neuron: dict | None = None
    studio: dict | None = None


# ─── Helpers ───
def _extract_claims(model: str, answer: str) -> list[dict[str, Any]]:
    """Extracts factual claims from the response."""
    claims = []
    sentences = re.split(r'(?<=[.!?])\s+', answer.strip())
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if len(sentence) < 10:
            continue
        claims.append({
            "id": f"claim_{i}",
            "proposition": f"prop_{i}",
            "value": True,
            "text": sentence,
            "evidence": sentence,
            "source": f"{model}_output"
        })
    
    return claims

async def _call_ollama(req: ChatRequest) -> str:
    """Calls Ollama to generate a response."""
    payload = {
        "model": req.model,
        "prompt": req.prompt,
        "stream": False,
        "options": {
            "num_predict": req.num_predict,
            "temperature": req.temperature
        }
    }
    if req.system:
        payload["system"] = req.system
    
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        resp = await client.post(f"{OLLAMA_BASE}/api/generate", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")


# ─── Routes ───
@app.get("/api/health")
async def health():
    """Health check with all modules status."""
    ollama_status = "unknown"
    models = []
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_BASE}/api/tags")
            if resp.status_code == 200:
                ollama_status = "connected"
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
    except Exception:
        ollama_status = "disconnected"
    
    return {
        "status": "ok",
        "project": "alpha0az1omega",
        "ollama": ollama_status,
        "verification_engine": "Z3",
        "modules": {
            "neuro_symbolic": True,
            "pgp": True,
            "epistemic": True,
            "studio": True
        },
        "models": models
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main endpoint: generates a response with full verification.
    Pipeline: Ollama → Z3 → PGP → Epistemic → Studio
    """
    try:
        # 1. Generation by model
        answer = await _call_ollama(req)
        
        if not answer.strip():
            raise HTTPException(status_code=502, detail="Empty response from model")
        
        # 2. Extract claims
        claims = _extract_claims(req.model, answer)
        
        # 3. Z3 verification
        verification = verify_response_claims(answer, claims)
        
        # 4. PGP signature (luminous neuron)
        pgp_neuron = sign_response(
            response_text=answer,
            metadata={"model": req.model, "verification": verification.get("status")}
        )
        
        # 5. Epistemic score
        epistemic = compute_epistemic_score(
            verification=verification,
            claims=claims,
            pgp_neuron=pgp_neuron,
            response_text=answer,
            metadata={"model": req.model}
        )
        
        # 6. Record in fabrication graph
        studio_record = studio.record_response(
            prompt=req.prompt,
            response=answer,
            verification=verification,
            epistemic=epistemic
        )
        
        return ChatResponse(
            model=req.model,
            response=answer,
            done=True,
            verification=verification,
            epistemic=epistemic,
            pgp_neuron=pgp_neuron,
            studio={"prompt_node": studio_record["prompt_node"],
                    "response_node": studio_record["response_node"]}
        )
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Model timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pgp/chain")
async def pgp_chain():
    """Returns the luminous neuron chain summary."""
    return get_chain_summary()


@app.get("/api/epistemic/log")
async def epistemic_log():
    """Returns the epistemic journal."""
    from CORE.epistemic.engine import LOG_FILE
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


@app.get("/api/studio/graph")
async def studio_graph():
    """Returns the fabrication graph."""
    return studio.explore()


@app.get("/api/studio/subgraph/{node_id}")
async def studio_subgraph(node_id: str, depth: int = 2):
    """Returns a subgraph around a node."""
    return studio.explore(node_id, depth)
