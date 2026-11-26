"""
Epistemic Core — ALPHA0AZ1OMEGA
Computes the epistemic confidence index (C) for each response.
Builds a documented failure tree.

Index C = f(verification, evidence, coherence, provenance)
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Epistemic journal
EPISTEMIC_LOG: list[dict] = []
LOG_FILE = Path(__file__).parent / "epistemic_log.json"


@dataclass
class FailureNode:
    """Node in the failure tree."""
    node_id: str
    description: str
    severity: str  # "none", "low", "medium", "high", "critical"
    children: list["FailureNode"] = field(default_factory=list)
    mitigated: bool = False
    evidence: str = ""
    
    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "description": self.description,
            "severity": self.severity,
            "mitigated": self.mitigated,
            "evidence": self.evidence,
            "children": [c.to_dict() for c in self.children]
        }


@dataclass
class EpistemicResult:
    """Complete epistemic evaluation result."""
    index_c: float  # 0.0 to 1.0
    confidence_label: str  # "HIGH", "MEDIUM", "LOW", "UNVERIFIED"
    verification_status: str
    evidence_count: int
    failure_tree: FailureNode
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "index_C": round(self.index_c, 4),
            "confidence": self.confidence_label,
            "verification": self.verification_status,
            "evidence_count": self.evidence_count,
            "failure_tree": self.failure_tree.to_dict(),
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class EpistemicEngine:
    """
    Epistemic engine: computes index C from multiple signals.
    
    Formula:
        C = w1*V + w2*E + w3*H + w4*P
    where:
        V = Z3 verification score (0 or 1)
        E = evidence richness (0 to 1)
        H = internal coherence (0 to 1)
        P = PGP provenance/authenticity (0 or 1)
    
    Default weights: w1=0.35, w2=0.25, w3=0.25, w4=0.15
    """
    
    WEIGHTS = {
        "verification": 0.35,
        "evidence": 0.25,
        "coherence": 0.25,
        "provenance": 0.15
    }
    
    def __init__(self, weights: dict | None = None):
        if weights:
            self.WEIGHTS.update(weights)
    
    def compute(
        self,
        verification: dict | None = None,
        claims: list[dict] | None = None,
        pgp_neuron: dict | None = None,
        response_text: str = "",
        metadata: dict | None = None
    ) -> EpistemicResult:
        """Computes the full index C."""
        
        # 1. Z3 verification score
        v_score, v_node = self._score_verification(verification)
        
        # 2. Evidence richness
        e_score, e_node = self._score_evidence(claims)
        
        # 3. Internal coherence
        h_score, h_node = self._score_coherence(response_text, claims)
        
        # 4. PGP provenance
        p_score, p_node = self._score_provenance(pgp_neuron)
        
        # Compute C
        index_c = (
            self.WEIGHTS["verification"] * v_score +
            self.WEIGHTS["evidence"] * e_score +
            self.WEIGHTS["coherence"] * h_score +
            self.WEIGHTS["provenance"] * p_score
        )
        
        # Confidence label
        if index_c >= 0.85:
            label = "HIGH"
        elif index_c >= 0.60:
            label = "MEDIUM"
        elif index_c >= 0.30:
            label = "LOW"
        else:
            label = "UNVERIFIED"
        
        # Failure tree root
        root = FailureNode(
            node_id="ROOT",
            description="Complete epistemic evaluation",
            severity="none",
            children=[v_node, e_node, h_node, p_node],
            evidence=f"C = {index_c:.4f} ({label})"
        )
        
        result = EpistemicResult(
            index_c=index_c,
            confidence_label=label,
            verification_status=verification.get("status", "UNKNOWN") if verification else "UNKNOWN",
            evidence_count=len(claims) if claims else 0,
            failure_tree=root,
            metadata=metadata or {}
        )
        
        # Logging
        self._log(result)
        
        return result
    
    def _score_verification(self, verification: dict | None) -> tuple[float, FailureNode]:
        """Z3 verification score."""
        if not verification:
            return 0.0, FailureNode(
                node_id="V1",
                description="Z3 verification missing",
                severity="high",
                evidence="No verification provided"
            )
        
        if verification.get("accepted"):
            return 1.0, FailureNode(
                node_id="V1",
                description="Z3 verification passed",
                severity="none",
                mitigated=True,
                evidence=f"Status: {verification.get('status')}, Claims: {verification.get('claim_count', 0)}"
            )
        else:
            return 0.0, FailureNode(
                node_id="V1",
                description="Z3 verification failed",
                severity="critical",
                evidence=f"Status: {verification.get('status', 'FAILED')}"
            )
    
    def _score_evidence(self, claims: list[dict] | None) -> tuple[float, FailureNode]:
        """Score based on evidence richness."""
        if not claims:
            return 0.3, FailureNode(
                node_id="E1",
                description="No claims extracted",
                severity="medium",
                evidence="Response without structured claims"
            )
        
        # Score proportional to claims with evidence
        with_evidence = sum(1 for c in claims if c.get("evidence"))
        ratio = with_evidence / len(claims) if claims else 0
        
        score = min(1.0, 0.4 + 0.6 * ratio)
        severity = "none" if ratio >= 0.8 else "low" if ratio >= 0.5 else "medium"
        
        return score, FailureNode(
            node_id="E1",
            description=f"Evidence: {with_evidence}/{len(claims)} claims with evidence",
            severity=severity,
            mitigated=ratio >= 0.8,
            evidence=f"Ratio: {ratio:.2f}"
        )
    
    def _score_coherence(self, text: str, claims: list[dict] | None) -> tuple[float, FailureNode]:
        """Internal coherence score."""
        if not text:
            return 0.0, FailureNode(
                node_id="H1",
                description="Empty response",
                severity="critical"
            )
        
        # Coherence heuristics
        issues = []
        
        # Check for basic contradictions in text
        text_lower = text.lower()
        contradiction_markers = ["but not", "however it is not", "contradicting", "which is false"]
        for marker in contradiction_markers:
            if marker in text_lower:
                issues.append(f"Contradiction marker: '{marker}'")
        
        # Minimum length
        if len(text) < 5:
            issues.append("Response too short")
        
        if issues:
            score = max(0.0, 1.0 - 0.3 * len(issues))
            return score, FailureNode(
                node_id="H1",
                description="Coherence issues detected",
                severity="medium" if len(issues) == 1 else "high",
                evidence="; ".join(issues)
            )
        
        return 1.0, FailureNode(
            node_id="H1",
            description="Internal coherence verified",
            severity="none",
            mitigated=True,
            evidence="No contradiction markers found"
        )
    
    def _score_provenance(self, neuron: dict | None) -> tuple[float, FailureNode]:
        """PGP provenance score."""
        if not neuron:
            return 0.5, FailureNode(
                node_id="P1",
                description="PGP signature missing",
                severity="low",
                evidence="Luminous neuron unsigned"
            )
        
        if neuron.get("pgp_signature"):
            return 1.0, FailureNode(
                node_id="P1",
                description="PGP signature present",
                severity="none",
                mitigated=True,
                evidence=f"Neuron #{neuron.get('index', '?')}"
            )
        else:
            return 0.5, FailureNode(
                node_id="P1",
                description="Neuron without PGP signature",
                severity="low",
                evidence="Private key not available at signing time"
            )
    
    def _log(self, result: EpistemicResult) -> None:
        """Logs the result."""
        global EPISTEMIC_LOG
        entry = result.to_dict()
        EPISTEMIC_LOG.append(entry)
        
        # Persist
        try:
            existing = []
            if LOG_FILE.exists():
                existing = json.loads(LOG_FILE.read_text())
            existing.append(entry)
            LOG_FILE.write_text(json.dumps(existing, indent=2))
        except Exception:
            pass


def compute_epistemic_score(
    verification: dict | None = None,
    claims: list[dict] | None = None,
    pgp_neuron: dict | None = None,
    response_text: str = "",
    metadata: dict | None = None
) -> dict:
    """Public function: computes and returns index C."""
    engine = EpistemicEngine()
    result = engine.compute(
        verification=verification,
        claims=claims,
        pgp_neuron=pgp_neuron,
        response_text=response_text,
        metadata=metadata
    )
    return result.to_dict()
