from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas import ThreatType, AnalyzeResponse, LLMThreatAnalysis

client = TestClient(app)

def test_analyze_endpoint_benign():
    # Mocking the LLM response
    mock_llm_result = LLMThreatAnalysis(
        threat_type=ThreatType.BENIGN,
        confidence=0.99,
        reason="The message is a standard greeting."
    )
    
    with patch("app.main.analyze_threat", return_value=mock_llm_result):
        response = client.post("/analyze", json={"message": "Hey, how are you?"})
        assert response.status_code == 200
        data = response.json()
        assert data["threat_type"] == "benign"
        assert data["confidence"] == 0.99
        assert data["risk_score"] == 0
        assert data["action"] == "allow"

def test_analyze_endpoint_phishing():
    # Mocking the LLM response
    mock_llm_result = LLMThreatAnalysis(
        threat_type=ThreatType.PHISHING,
        confidence=0.95,
        reason="The message contains urgency and suspicious link."
    )
    
    with patch("app.main.analyze_threat", return_value=mock_llm_result):
        response = client.post("/analyze", json={"message": "Your account is locked. Click here now."})
        assert response.status_code == 200
        data = response.json()
        assert data["threat_type"] == "phishing"
        # 1.0 * 0.95 * 100 = 95 -> BLOCK
        assert data["risk_score"] == 95
        assert data["action"] == "block"

def test_analyze_invalid_input():
    response = client.post("/analyze", json={"message": ""})
    assert response.status_code == 422  # Validation error for empty string (min_length=1)

def test_analyze_missing_field():
    response = client.post("/analyze", json={})
    assert response.status_code == 422
