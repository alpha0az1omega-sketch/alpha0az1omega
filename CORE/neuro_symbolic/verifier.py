from __future__ import annotations

import re
from typing import Any

from z3 import Bool, Not, Solver, sat, unsat

PROPOSITION_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,95}$")
MAX_CLAIMS = 100


def _rejected(status: str, reason: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "status": status,
        "solver": "Z3",
        "reason": reason,
        "scope": "logical_consistency_only",
    }


def verify_claims(claims: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(claims, list) or not claims:
        return _rejected("UNVERIFIED_EMPTY", "No formal claims supplied.")

    if len(claims) > MAX_CLAIMS:
        return _rejected("INVALID_INPUT", "Claim limit exceeded.")

    solver = Solver()
    solver.set(timeout=2000)

    symbols = {}
    labels = {}

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            return _rejected("INVALID_INPUT", "Claim must be an object.")

        proposition = claim.get("proposition")
        value = claim.get("value")

        if (
            not isinstance(proposition, str)
            or not PROPOSITION_PATTERN.fullmatch(proposition)
        ):
            return _rejected("INVALID_INPUT", "Invalid proposition identifier.")

        if type(value) is not bool:
            return _rejected("INVALID_INPUT", "Claim value must be boolean.")

        symbol = symbols.setdefault(proposition, Bool(proposition))
        formula = symbol if value else Not(symbol)

        label = Bool(f"claim_{index}")
        solver.assert_and_track(formula, label)
        labels[str(label)] = {
            "proposition": proposition,
            "value": value,
        }

    result = solver.check()

    if result == sat:
        return {
            "accepted": True,
            "status": "CONSISTENT",
            "solver": "Z3",
            "claim_count": len(claims),
            "scope": "logical_consistency_only",
        }

    if result == unsat:
        conflicts = [
            labels[str(item)]
            for item in solver.unsat_core()
            if str(item) in labels
        ]

        return {
            "accepted": False,
            "status": "CONTRADICTION",
            "solver": "Z3",
            "claim_count": len(claims),
            "conflicts": conflicts,
            "scope": "logical_consistency_only",
        }

    return _rejected(
        "UNKNOWN",
        f"Z3 could not decide: {solver.reason_unknown()}",
    )


def verify_response_claims(
    response_text: str,
    claims: list[dict[str, Any]],
) -> dict[str, Any]:

    if not isinstance(response_text, str) or not response_text.strip():
        return _rejected("INVALID_RESPONSE", "Empty assistant response.")

    if not isinstance(claims, list) or not claims:
        return _rejected(
            "UNVERIFIED_EMPTY",
            "No machine-checkable claims were extracted.",
        )

    if len(claims) > MAX_CLAIMS:
        return _rejected("INVALID_INPUT", "Claim limit exceeded.")

    normalized_claims = []

    for claim in claims:
        if not isinstance(claim, dict):
            return _rejected("INVALID_EXTRACTION", "Invalid claim object.")

        proposition = claim.get("proposition")
        value = claim.get("value")
        evidence = claim.get("evidence")

        if not isinstance(evidence, str) or not evidence.strip():
            return _rejected("INVALID_EVIDENCE", "Missing evidence quotation.")

        if evidence not in response_text:
            return _rejected(
                "INVALID_EVIDENCE",
                "Evidence quotation is not present in the assistant response.",
            )

        normalized_claims.append({
            "proposition": proposition,
            "value": value,
        })

    result = verify_claims(normalized_claims)
    result["evidence_quotes_checked"] = len(claims)

    return result
