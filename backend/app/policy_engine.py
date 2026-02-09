from app.schemas import Action

def determine_action(risk_score: int) -> Action:
    """
    Determines action based on risk score thresholds.
    >= 80: BLOCK
    >= 50: FLAG
    < 50: ALLOW
    """
    if risk_score >= 80:
        return Action.BLOCK
    elif risk_score >= 50:
        return Action.FLAG
    else:
        return Action.ALLOW
