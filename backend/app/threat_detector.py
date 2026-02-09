import json
import google.generativeai as genai
from app.config import settings
from app.schemas import LLMThreatAnalysis, ThreatType

# Configure Gemini
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
else:
    # Handle missing API key gracefully, possibly raise an error or warn
    print("Warning: GOOGLE_API_KEY not set in environment variables.")

model_name = "gemini-3-flash-preview" 

def get_model():
    # Helper to get model instance, ensures lazy loading if needed
    return genai.GenerativeModel(
        model_name,
        generation_config={"response_mime_type": "application/json", "temperature": 0.0}
    )

def analyze_threat(text: str, preprocessed_data: dict) -> LLMThreatAnalysis:
    try:
        model = get_model()
        
        prompt = f"""
        You are a cybersecurity expert analyzing chat messages for threats.
        
        Input Context:
        Message: "{text}"
        Preprocessed Data: {json.dumps(preprocessed_data)}
        
        Task: Classify the message into exactly ONE of the following categories:
        - phishing: credential harvesting or account takeover
        - scam: financial or social engineering fraud
        - malware: malicious downloads or links
        - impersonation: pretending to be authority or trusted entity
        - prompt_injection: attempts to override AI instructions
        - benign: no threat detected

        Prioritize safety. If uncertain, classify conservatively (e.g., if it looks like phishing but you are not sure, mark as phishing or scam rather than benign, usually). However, "benign" should be used for normal conversation.
        
        Output Requirements:
        - Return ONLY valid JSON.
        - format: {{"threat_type": "<category>", "confidence": <float 0.0-1.0>, "reason": "<one sentence explanation>"}}
        - threat_type must be one of the keys strictly.
        """

        response = model.generate_content(prompt)
        
        # Parse the JSON response
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback if model fails to output valid JSON (unlikely with json mode)
            return LLMThreatAnalysis(
                threat_type=ThreatType.BENIGN,
                confidence=0.0,
                reason="Error parsing model response"
            )

        # Validate against schema
        return LLMThreatAnalysis(
            threat_type=ThreatType(result.get("threat_type", "benign")),
            confidence=float(result.get("confidence", 0.0)),
            reason=result.get("reason", "No reason provided")
        )

    except Exception as e:
        # Fail safe
        print(f"Error in threat detection: {e}")
        return LLMThreatAnalysis(
            threat_type=ThreatType.BENIGN,
            confidence=0.0,
            reason=f"Internal error: {str(e)}"
        )
