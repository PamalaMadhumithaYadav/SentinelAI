from app.schemas import ThreatType

THREAT_SEVERITY = {
    ThreatType.PHISHING: 1.0,
    ThreatType.MALWARE: 1.0,
    ThreatType.SCAM: 0.8,
    ThreatType.IMPERSONATION: 0.8,
    ThreatType.PROMPT_INJECTION: 0.7,
    ThreatType.BENIGN: 0.0
}

def calculate_risk_score(threat_type: ThreatType, confidence: float) -> int:
    """
    Calculates a risk score between 0 and 100.
    Formula: Severity * Confidence * 100
    """
    severity = THREAT_SEVERITY.get(threat_type, 0.0)
    # Ensure confidence is within 0.0 - 1.0 (though schema enforces it)
    confidence = max(0.0, min(1.0, confidence))
    
    score = int(severity * confidence * 100)
    return max(0, min(100, score))
