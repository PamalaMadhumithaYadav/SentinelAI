from enum import Enum
from pydantic import BaseModel, Field

class ThreatType(str, Enum):
    PHISHING = "phishing"
    SCAM = "scam"
    MALWARE = "malware"
    IMPERSONATION = "impersonation"
    PROMPT_INJECTION = "prompt_injection"
    BENIGN = "benign"

class Action(str, Enum):
    BLOCK = "block"
    FLAG = "flag"
    ALLOW = "allow"

class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The chat message to analyze")

class LLMThreatAnalysis(BaseModel):
    threat_type: ThreatType
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str

class DecisionTrace(BaseModel):
    llm_threat: ThreatType
    confidence: float
    risk_score: int
    base_action: Action
    memory_hits: int
    final_action: Action

class AnalyzeResponse(LLMThreatAnalysis):
    request_id: str
    risk_score: int = Field(..., ge=0, le=100)
    action: Action
    confidence_level: ConfidenceLevel
    decision_trace: DecisionTrace
