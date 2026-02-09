from app.schemas import ThreatType, Action
from app.risk_engine import calculate_risk_score
from app.policy_engine import determine_action

def test_risk_calculation_phishing_high_confidence():
    score = calculate_risk_score(ThreatType.PHISHING, 0.9)
    # 1.0 * 0.9 * 100 = 90
    assert score == 90

def test_risk_calculation_benign():
    score = calculate_risk_score(ThreatType.BENIGN, 1.0)
    # 0.0 * 1.0 * 100 = 0
    assert score == 0

def test_risk_calculation_scam_medium_confidence():
    score = calculate_risk_score(ThreatType.SCAM, 0.5)
    # 0.8 * 0.5 * 100 = 40
    assert score == 40

def test_policy_determination_block():
    action = determine_action(90)
    assert action == Action.BLOCK

def test_policy_determination_flag():
    action = determine_action(70)
    assert action == Action.FLAG
    
    action = determine_action(50)
    assert action == Action.FLAG

def test_policy_determination_allow():
    action = determine_action(49)
    assert action == Action.ALLOW
    
    action = determine_action(0)
    assert action == Action.ALLOW
