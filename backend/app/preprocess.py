import re
from typing import List, Dict

def extract_urls(text: str) -> List[str]:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.findall(text)

def detect_urgency(text: str) -> bool:
    urgency_keywords = ["urgent", "now", "immediately", "hurry", "act fast", "quick", "deadline", "expire"]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in urgency_keywords)

def detect_authority(text: str) -> bool:
    authority_keywords = ["admin", "it team", "support", "security team", "ceo", "hr", "manager"]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in authority_keywords)

def preprocess_message(text: str) -> Dict:
    return {
        "urls": extract_urls(text),
        "has_urgency": detect_urgency(text),
        "claims_authority": detect_authority(text),
        "original_text": text
    }
