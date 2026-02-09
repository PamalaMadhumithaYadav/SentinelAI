import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import ThreatType, Action, LLMThreatAnalysis

client = TestClient(app)
LOG_FILE = Path("logs/audit.log")

def setup_module():
    # Ensure logs directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Clear log file before tests
    if LOG_FILE.exists():
        LOG_FILE.unlink()

def teardown_module():
    if LOG_FILE.exists():
        LOG_FILE.unlink()

def test_audit_log_entry_created():
    # Mock LLM
    mock_llm = LLMThreatAnalysis(
        threat_type=ThreatType.BENIGN,
        confidence=0.9,
        reason="Safe"
    )
    
    with patch("app.main.analyze_threat", return_value=mock_llm):
        response = client.post("/analyze", json={"message": "Audit test message"})
        assert response.status_code == 200
        data = response.json()
        
        request_id = data["request_id"]
        assert request_id is not None
        
        # Verify log file content
        assert LOG_FILE.exists()
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            last_line = lines[-1]
            log_entry = json.loads(last_line)
            
            assert log_entry["request_id"] == request_id
            assert log_entry["message_hash"] is not None
            assert log_entry["message_hash"] != "Audit test message" # Hashed
            assert log_entry["threat_type"] == "benign"
            assert "timestamp" in log_entry

def test_audit_log_fail_safe():
    # Simulate IO Error during logging
    mock_llm = LLMThreatAnalysis(
        threat_type=ThreatType.PHISHING,
        confidence=0.95,
        reason="Bad"
    )
    
    with patch("app.main.analyze_threat", return_value=mock_llm):
        with patch("builtins.open", side_effect=IOError("Disk full")):
            # The API should still return 200 OK
            response = client.post("/analyze", json={"message": "Fail safe test"})
            assert response.status_code == 200
            data = response.json()
            assert data["threat_type"] == "phishing"
            assert data["request_id"] is not None
