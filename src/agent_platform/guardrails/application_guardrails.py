# agent_platform/guardrails/application_guardrails.py

import re
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

# =====================================================
# Result Contract
# =====================================================


@dataclass
class PreGuardrailResult:
    allowed: bool
    query: Optional[str]
    metadata: Dict


# =====================================================
# Core Pre-Agent Guardrail Pipeline
# =====================================================


def run_pre_agent_guardrails(query: str, customer_id: str) -> PreGuardrailResult:
    """
    Pre-agent safety + normalization layer.

    Responsibilities:
    - Prompt injection detection
    - PII detection + redaction
    - Basic input validation
    - Optional routing metadata
    """

    metadata: Dict = {
        "customer_id": customer_id,
        "blocked": False,
        "reasons": [],
        "detected_pii": {},
        "route": None,
    }

    # -------------------------------------------------
    # 1. Input validation
    # -------------------------------------------------
    if query is None or not query.strip():
        return PreGuardrailResult(
            allowed=False,
            query=None,
            metadata={"reason": "Empty query"},
        )

    cleaned_query = query.strip()

    # -------------------------------------------------
    # 2. Prompt injection detection
    # -------------------------------------------------
    injection_patterns = [
        r"ignore (previous|all) instructions",
        r"disregard (previous|all) instructions",
        r"you are now",
        r"system prompt",
        r"developer message",
        r"reveal (your|the) prompt",
        r"show (your|the) instructions",
        r"bypass (safety|guardrails)",
        r"act as if",
    ]

    for pattern in injection_patterns:
        if re.search(pattern, cleaned_query, re.IGNORECASE):
            metadata["blocked"] = True
            metadata["reasons"].append(f"injection_detected: {pattern}")

    # -------------------------------------------------
    # 3. PII Detection
    # -------------------------------------------------
    pii_patterns = {
        "card_number": r"\b(?:\d{4}[- ]?){3}\d{4}\b|\b\d{13,19}\b",
        "sin": r"\b\d{3}[- ]?\d{3}[- ]?\d{3}\b",
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "phone": r"\b(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{3}\)?)[-.\s]?\d{3}[-.\s]?\d{4}\b",
    }

    detected_pii = {}

    for pii_type, pattern in pii_patterns.items():
        matches = re.findall(pattern, cleaned_query)
        if matches:
            detected_pii[pii_type] = len(matches)

    metadata["detected_pii"] = detected_pii

    # -------------------------------------------------
    # 4. Block decision
    # -------------------------------------------------
    if metadata["blocked"]:
        return PreGuardrailResult(
            allowed=False,
            query=None,
            metadata=metadata,
        )

    # -------------------------------------------------
    # 5. Redaction (safe version passed to agents)
    # -------------------------------------------------
    cleaned_query = mask_pii_in_text(cleaned_query)

    # -------------------------------------------------
    # 6. Optional routing layer (extensible)
    # -------------------------------------------------
    metadata["route"] = classify_route(cleaned_query)

    return PreGuardrailResult(
        allowed=True,
        query=cleaned_query,
        metadata=metadata,
    )


# =====================================================
# Routing (optional but useful for multi-agent systems)
# =====================================================


def classify_route(query: str) -> str:
    """
    Simple deterministic router.
    Can later be replaced with LLM classifier.
    """

    q = query.lower()

    if any(x in q for x in ["password", "login", "sign in"]):
        return "auth_support"

    if any(x in q for x in ["balance", "transaction", "account", "statement"]):
        return "account_support"

    if any(x in q for x in ["crash", "error", "bug", "not working"]):
        return "technical_support"

    return "general_support"


# =====================================================
# PII Masking Layer
# =====================================================


def mask_pii_in_text(text: str) -> str:
    text = mask_card_numbers(text)
    text = mask_account_numbers(text)
    text = mask_email(text)
    return text


def mask_card_numbers(text: str) -> str:
    pattern = re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b|\b\d{13,19}\b")

    return pattern.sub(
        lambda m: mask_card_number(m.group()),
        text,
    )


def mask_card_number(card_number: str) -> str:
    digits = re.sub(r"\D", "", card_number)

    if len(digits) < 13 or len(digits) > 19:
        return card_number

    masked = "*" * (len(digits) - 4) + digits[-4:]

    result = []
    i = 0

    for ch in card_number:
        if ch.isdigit():
            result.append(masked[i])
            i += 1
        else:
            result.append(ch)

    return "".join(result)


def mask_account_numbers(text: str) -> str:
    pattern = re.compile(
        r"(account\s*(?:number|#)?\s*[:=]?\s*)(\d{8,20})",
        re.IGNORECASE,
    )

    return pattern.sub(
        lambda m: f"{m.group(1)}****{m.group(2)[-4:]}",
        text,
    )


def mask_email(text: str) -> str:
    pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    return pattern.sub("[REDACTED_EMAIL]", text)


# =====================================================
# Convenience Wrapper for Application Layer
# =====================================================


def apply_pre_guardrails(query: str, customer_id: str) -> PreGuardrailResult:
    """
    Public API used by application layer (CrewAI entrypoint).
    """
    return run_pre_agent_guardrails(query, customer_id)
