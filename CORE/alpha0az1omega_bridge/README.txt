ALPHA0AZ1OMEGA — LOCAL OLLAMA BRIDGE (starter)

This adds a local FastAPI bridge. It does NOT edit VISUAL/index.html and does NOT
claim that Z3/Lean/PGP/zkML verification is implemented.

1) Copy CORE/bridge.py into:
   ~/alpha0az1omega/CORE/bridge.py

2) From the project root, start the local server:
   cd ~/alpha0az1omega
   python3 -m uvicorn CORE.bridge:app --host 127.0.0.1 --port 8000

3) In a second Terminal tab, check the bridge and Ollama:
   curl -sS --max-time 10 http://127.0.0.1:8000/api/health

4) Test an actual model response through FastAPI:
   curl -sS --max-time 240 http://127.0.0.1:8000/api/chat \
     -H 'Content-Type: application/json' \
     -d '{"model":"qwen3.8:27b","prompt":"Réponds exactement : NEXUS_BRIDGE_OK"}'

5) Open the existing V19 page locally:
   http://127.0.0.1:8000/

IMPORTANT
- Keep the server bound to 127.0.0.1. Do not change it to 0.0.0.0.
- Do not set OLLAMA_ORIGINS="*".
- Do not expose port 11434 or 8000 to the Internet.
- At this stage the bridge API is functional, but V19's terminal is not wired to
  /api/chat yet. The visible HTML should only be patched after its current JS
  input handler has been inspected and backed up.
