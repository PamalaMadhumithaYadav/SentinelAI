from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas import ThreatType, Action, LLMThreatAnalysis

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_decision_trace_and_confidence():
    mock_llm = LLMThreatAnalysis(
        threat_type=ThreatType.PHISHING,
        confidence=0.95,
        reason="Bad link"
    )
    
    # Mocking analyze_threat to return specific confidence
    with patch("app.main.analyze_threat", return_value=mock_llm):
        # Mocking memory to return 0 hits
        with patch("app.main.evaluate_memory", return_value=(Action.BLOCK, 0)): 
            # Note: mocking evaluate_memory to return BLOCK to match expected final action if base is BLOCK
            # Wait, calculate_risk_score(PHISHING, 0.95) -> 95 -> BLOCK.
            
            response = client.post("/analyze", json={"message": "Test message"})
            assert response.status_code == 200
            data = response.json()
            
            # Verify Confidence Level
            assert data["confidence_level"] == "high"
            
            # Verify Decision Trace
            trace = data["decision_trace"]
            assert trace["llm_threat"] == "phishing"
            assert trace["confidence"] == 0.95
            assert trace["risk_score"] == 95
            assert trace["base_action"] == "block"
            assert trace["memory_hits"] == 0
            assert trace["final_action"] == "block"

def test_confidence_level_buckets():
    # Test Medium
    mock_llm_med = LLMThreatAnalysis(threat_type=ThreatType.SCAM, confidence=0.5, reason="Maybe")
    with patch("app.main.analyze_threat", return_value=mock_llm_med):
         with patch("app.main.evaluate_memory", return_value=(Action.FLAG, 0)):
            response = client.post("/analyze", json={"message": "med"})
            assert response.json()["confidence_level"] == "medium"

    # Test Low
    mock_llm_low = LLMThreatAnalysis(threat_type=ThreatType.BENIGN, confidence=0.1, reason="Safe")
    with patch("app.main.analyze_threat", return_value=mock_llm_low):
         with patch("app.main.evaluate_memory", return_value=(Action.ALLOW, 0)):
            response = client.post("/analyze", json={"message": "low"})
            assert response.json()["confidence_level"] == "low"
