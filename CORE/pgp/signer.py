"""
PGP Signer — ALPHA0AZ1OMEGA
Signs every system response and verifies authenticity.
Creates "luminous neurons": chained signature fingerprints.
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any

# Key paths
KEY_DIR = Path(__file__).parent / "keys"
PUBLIC_KEY = KEY_DIR / "alpha0az1omega_owner_public.asc"
PRIVATE_KEY = KEY_DIR / "alpha0az1omega_owner_private.asc"

# Luminous neuron chain (each signature points to the previous one)
LUMINOUS_NEURONS: list[dict[str, Any]] = []
NEURON_CHAIN_FILE = Path(__file__).parent / "neuron_chain.json"


def _load_chain() -> list[dict]:
    """Loads the existing neuron chain."""
    if NEURON_CHAIN_FILE.exists():
        return json.loads(NEURON_CHAIN_FILE.read_text())
    return []


def _save_chain(chain: list[dict]) -> None:
    """Persists the neuron chain."""
    NEURON_CHAIN_FILE.write_text(json.dumps(chain, indent=2))


def _compute_content_hash(content: str) -> str:
    """SHA-256 hash of the content to sign."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def sign_response(response_text: str, metadata: dict | None = None) -> dict[str, Any]:
    """
    Signs a response with the PGP private key.
    Returns a luminous neuron containing:
    - Content hash
    - PGP signature (if private key available)
    - Link to previous neuron
    - Timestamp
    """
    global LUMINOUS_NEURONS
    
    chain = _load_chain()
    content_hash = _compute_content_hash(response_text)
    timestamp = time.time()
    
    # Link to previous neuron
    prev_hash = chain[-1]["content_hash"] if chain else "ROOT"
    
    # PGP signature (if private key available)
    pgp_signature = None
    if PRIVATE_KEY.exists():
        try:
            payload = f"{content_hash}:{prev_hash}:{timestamp}"
            result = subprocess.run(
                ["gpg", "--batch", "--yes", "--detach-sign", "--armor",
                 "--local-user", "alpha0az1omega@gmail.com"],
                input=payload.encode(),
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                pgp_signature = result.stdout.decode("utf-8")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pgp_signature = None
    
    # Create luminous neuron
    neuron = {
        "index": len(chain),
        "content_hash": content_hash,
        "previous_neuron": prev_hash,
        "timestamp": timestamp,
        "pgp_signature": pgp_signature,
        "metadata": metadata or {},
        "response_preview": response_text[:120] + "..." if len(response_text) > 120 else response_text
    }
    
    chain.append(neuron)
    _save_chain(chain)
    LUMINOUS_NEURONS = chain
    
    return neuron


def verify_signature(neuron: dict) -> dict[str, Any]:
    """
    Verifies the authenticity of a luminous neuron.
    Checks:
    1. Chain consistency (previous_neuron)
    2. PGP signature (if present)
    """
    result = {
        "neuron_index": neuron.get("index"),
        "chain_valid": False,
        "pgp_valid": False,
        "overall": "UNVERIFIED"
    }
    
    # Chain verification
    chain = _load_chain()
    idx = neuron.get("index", 0)
    
    if idx == 0 and neuron.get("previous_neuron") == "ROOT":
        result["chain_valid"] = True
    elif idx > 0 and idx < len(chain):
        expected_prev = chain[idx - 1]["content_hash"]
        result["chain_valid"] = (neuron.get("previous_neuron") == expected_prev)
    
    # PGP verification
    if neuron.get("pgp_signature") and PUBLIC_KEY.exists():
        try:
            payload = f"{neuron['content_hash']}:{neuron['previous_neuron']}:{neuron['timestamp']}"
            sig_file = Path("/tmp/alpha0az1omega_verify.sig")
            sig_file.write_text(neuron["pgp_signature"])
            
            proc = subprocess.run(
                ["gpg", "--batch", "--verify", str(sig_file), "-"],
                input=payload.encode(),
                capture_output=True,
                timeout=10
            )
            result["pgp_valid"] = (proc.returncode == 0)
            sig_file.unlink(missing_ok=True)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            result["pgp_valid"] = False
    
    # Global verdict
    if result["chain_valid"] and result["pgp_valid"]:
        result["overall"] = "AUTHENTIC"
    elif result["chain_valid"]:
        result["overall"] = "CHAIN_VALID_NO_PGP"
    else:
        result["overall"] = "INVALID"
    
    return result


def get_chain_summary() -> dict[str, Any]:
    """Returns a summary of the luminous neuron chain."""
    chain = _load_chain()
    return {
        "total_neurons": len(chain),
        "first_neuron": chain[0]["content_hash"][:16] + "..." if chain else None,
        "last_neuron": chain[-1]["content_hash"][:16] + "..." if chain else None,
        "signed_neurons": sum(1 for n in chain if n.get("pgp_signature")),
        "chain_integrity": _verify_full_chain()
    }


def _verify_full_chain() -> bool:
    """Verifies the full chain integrity."""
    chain = _load_chain()
    if not chain:
        return True
    
    if chain[0].get("previous_neuron") != "ROOT":
        return False
    
    for i in range(1, len(chain)):
        if chain[i].get("previous_neuron") != chain[i-1]["content_hash"]:
            return False
    
    return True
