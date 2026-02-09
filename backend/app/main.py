from fastapi import FastAPI, HTTPException
import uuid
from app.schemas import AnalyzeRequest, AnalyzeResponse, DecisionTrace, ConfidenceLevel
from app.preprocess import preprocess_message
from app.threat_detector import analyze_threat, model_name
from app.risk_engine import calculate_risk_score
from app.policy_engine import determine_action
from app.memory_engine import evaluate_memory
from app.audit_logger import log_event, hash_message
import uvicorn
from app.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chat Security Agent",
    description="Real-time chat threat detection API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chat-security-frontend-175245796032.us-central1.run.app"
    ], # Allow all origins for dev, or specific ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_confidence_level(confidence: float) -> ConfidenceLevel:
    if confidence >= 0.7:
        return ConfidenceLevel.HIGH
    elif confidence >= 0.4:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW

@app.get("/")
def read_root():
    return {"message": "Chat Security Agent API is running. Use POST /analyze to scan messages."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message_endpoint(request: AnalyzeRequest):
    request_id = str(uuid.uuid4())
    try:
        # Preprocessing
        preprocessed_data = preprocess_message(request.message)
        
        # Threat Detection via LLM
        llm_result = analyze_threat(request.message, preprocessed_data)
        
        # Risk Scoring & Policy
        risk_score = calculate_risk_score(llm_result.threat_type, llm_result.confidence)
        base_action = determine_action(risk_score)
        
        # Memory Escalation (Phase 4 & 5)
        msg_hash = hash_message(request.message)
        final_action, memory_hits = evaluate_memory(msg_hash, llm_result.threat_type, base_action)
        
        # Explainability (Phase 5)
        confidence_level = get_confidence_level(llm_result.confidence)
        decision_trace = DecisionTrace(
            llm_threat=llm_result.threat_type,
            confidence=llm_result.confidence,
            risk_score=risk_score,
            base_action=base_action,
            memory_hits=memory_hits,
            final_action=final_action
        )

        # Audit Logging (Safe)
        signals = []
        if preprocessed_data.get("has_urgency"):
            signals.append("urgency")
        if preprocessed_data.get("claims_authority"):
            signals.append("authority_claim")
            
        log_event(
            request_id=request_id,
            message=request.message,
            threat_type=llm_result.threat_type,
            confidence=llm_result.confidence,
            risk_score=risk_score,
            action=final_action,
            signals=signals,
            model_name=model_name,
            confidence_level=confidence_level,
            decision_trace=decision_trace,
            base_action=base_action
        )
        
        return AnalyzeResponse(
            **llm_result.model_dump(),
            risk_score=risk_score,
            action=final_action,
            request_id=request_id,
            confidence_level=confidence_level,
            decision_trace=decision_trace
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
