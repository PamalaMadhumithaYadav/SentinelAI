import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from app.schemas import ThreatType, Action, DecisionTrace, ConfidenceLevel

LOG_FILE = Path("logs/audit.log")

def hash_message(message: str) -> str:
    """Calculates SHA-256 hash of the message."""
    return hashlib.sha256(message.encode("utf-8")).hexdigest()

def log_event(
    request_id: str,
    message: str,
    threat_type: ThreatType,
    confidence: float,
    risk_score: int,
    action: Action,
    signals: List[str],
    model_name: str,
    confidence_level: ConfidenceLevel,
    decision_trace: DecisionTrace,
    base_action: Optional[Action] = None
) -> None:
    """
    Appends an audit record to the log file.
    Fail-safe: Catches all exceptions to prevent API failure.
    """
    try:
        # Create structured record
        record = {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(), # Explicit UTC
            "message_hash": hash_message(message),
            "threat_type": threat_type.value,
            "confidence": confidence,
            "risk_score": risk_score,
            "action": action.value,
            "signals": signals,
            "model": model_name,
            "confidence_level": confidence_level.value,
            "decision_trace": decision_trace.model_dump()
        }
        
        # Log base_action if escalation occurred
        if base_action and base_action != action:
            record["base_action"] = base_action.value
            record["final_action"] = action.value
            # Remove redundant "action" key if we want strict schema match or keep it as "action" (final)
            # The requirement says: final_action should be logged.
            # "Each audit entry MUST reflect the final escalated action."
            # "If base_action == final_action, log normally."
            # Example shows: "base_action": "flag", "final_action": "block"
            # It implies we should replace "action" with "final_action" OR keep "action" as final.
            # To be safe and compatible with previous logs, I will keep "action" as final,
            # and ADD "base_action" and "final_action" (redundant but explicit) if escalated.
        
        # Ensure directory exists (redundant safety)
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Append to file
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    except Exception as e:
        # Silent failure as per requirement: "Logging failures MUST NOT break the API"
        # In a real system, might log this to stderr or system log
        print(f"AUDIT LOG FAILURE: {e}")
