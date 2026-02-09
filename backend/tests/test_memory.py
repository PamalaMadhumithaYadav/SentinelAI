import json
import pytest
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from app.memory_engine import evaluate_memory, LOG_FILE
from app.schemas import Action, ThreatType

# Use a temporary log file for testing
TEST_LOG_FILE = Path("logs/test_audit.log")

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: Point LOG_FILE to test file (by patching)
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        if TEST_LOG_FILE.exists():
            TEST_LOG_FILE.unlink()
        TEST_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        yield
        # Teardown
        if TEST_LOG_FILE.exists():
            TEST_LOG_FILE.unlink()

def _append_log(message_hash: str, count: int, minutes_ago: int = 0):
    timestamp = (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()
    record = {
        "message_hash": message_hash,
        "timestamp": timestamp,
        "threat_type": "phishing", # Dummy for counting
        "action": "flag" # Dummy
    }
    with open(TEST_LOG_FILE, "a") as f:
        for _ in range(count):
            f.write(json.dumps(record) + "\n")

def test_escalation_rule_1_flag_to_block():
    msg_hash = "hash1"
    # Log 2 previous attempts (total will be 3 with current)
    _append_log(msg_hash, 2)
    
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        # Base action FLAG, total count 3 -> BLOCK
        final_action, count = evaluate_memory(msg_hash, ThreatType.SCAM, Action.FLAG)
        assert final_action == Action.BLOCK
        assert count == 3

def test_escalation_rule_1_flag_no_escalation():
    msg_hash = "hash2"
    # Log 1 previous attempt (total 2)
    _append_log(msg_hash, 1)
    
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        # Base action FLAG, total count 2 -> FLAG (no change)
        final_action, count = evaluate_memory(msg_hash, ThreatType.SCAM, Action.FLAG)
        assert final_action == Action.FLAG
        assert count == 2

def test_escalation_rule_2_high_risk_block():
    msg_hash = "hash3"
    # Log 4 previous attempts (total 5)
    _append_log(msg_hash, 4)
    
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        # Threat PHISHING, total count 5 -> BLOCK
        # Even if base action was ALLOW (unlikely but logic holds) or FLAG
        final_action, count = evaluate_memory(msg_hash, ThreatType.PHISHING, Action.FLAG)
        assert final_action == Action.BLOCK
        assert count == 5

def test_escalation_rule_3_benign_safe():
    msg_hash = "hash_benign"
    _append_log(msg_hash, 100) # Spamming benign
    
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        final_action, count = evaluate_memory(msg_hash, ThreatType.BENIGN, Action.ALLOW)
        assert final_action == Action.ALLOW
        assert count == 101

def test_memory_window_expiry():
    msg_hash = "hash_old"
    # Log 5 attempts but 20 minutes ago
    _append_log(msg_hash, 5, minutes_ago=20)
    
    with patch("app.memory_engine.LOG_FILE", TEST_LOG_FILE):
        final_action, count = evaluate_memory(msg_hash, ThreatType.PHISHING, Action.FLAG)
        # Should NOT count old logs, so total count = 1 -> No escalation
        assert final_action == Action.FLAG
        assert count == 1
