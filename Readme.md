# 🛡️ SentinelAI  
### Real-Time Chat Security Agent Powered by Gemini 3

SentinelAI is a **production-grade, real-time chat security agent** that detects phishing, scams, malware, impersonation, and prompt injection attacks in chat-based communication.

Unlike traditional keyword filters or generic AI chatbots, SentinelAI uses **Gemini 3 as a reasoning engine** to understand intent, assess risk, and enforce deterministic security decisions — **ALLOW, FLAG, or BLOCK** — with full transparency.

🏆 Built for the **Gemini 3 Global Hackathon**

---

## 🚨 The Problem

Cyber threats no longer arrive as obvious malware.

They arrive as:
- Phishing emails
- Scam messages from “trusted” contacts
- Urgent payment requests
- Prompt injection attacks targeting AI systems

Traditional security tools fail because:
- Rules (regex, keywords) are too rigid
- Raw LLMs are too unpredictable for security enforcement

Security systems must now understand **intent**, not just text.

---

## 💡 The Solution: SentinelAI

SentinelAI acts as an **intelligent firewall for conversations**.

It sits between users and applications, analyzing messages in real time and making **clear, explainable security decisions** backed by AI reasoning and deterministic policy logic.

---

## 🧠 Gemini 3 Integration (Core Innovation)

Gemini 3 is the **heart of SentinelAI**.

We use Gemini 3 **not as a chatbot**, but as a **reasoning engine** responsible for:

- Understanding social engineering patterns  
- Detecting urgency, impersonation, and manipulation  
- Identifying prompt injection attempts  
- Producing **structured JSON outputs** (threat type, confidence, reasoning)

These structured outputs are then consumed by SentinelAI’s deterministic engines to ensure decisions are:
- Machine-readable
- Auditable
- Safe for production use

Without Gemini 3’s advanced reasoning capabilities, SentinelAI would not be possible.

---

## 🏗️ System Architecture
User Browser
↓
Next.js Frontend (Cloud Run)
↓  /analyze
FastAPI Backend (Cloud Run)
↓
Deterministic Preprocessing
↓
Gemini 3 Reasoning Engine
↓
Risk Scoring Engine (0–100)
↓
Policy Engine (ALLOW / FLAG / BLOCK)
↓
Audit Logging + Memory Escalation

---

## 🔍 Core Features

### ✅ Threat Detection
Classifies messages into:
- Phishing
- Scam
- Malware
- Impersonation
- Prompt Injection
- Benign

### 📊 Risk Scoring
- Numerical risk score (0–100)
- Based on severity × Gemini confidence

### 🚦 Policy Engine
- **ALLOW** – Safe content
- **FLAG** – Suspicious content
- **BLOCK** – Dangerous content

### 🧠 Memory Escalation
- Repeated suspicious behavior escalates automatically
- Example: 3 FLAGS → BLOCK

### 📝 Audit Logging
- SHA-256 hashed message logging
- Append-only audit trail
- Full decision trace for explainability

---

## 🧪 Example

Your account is locked. Click here immediately to verify.

**Output:**
{
  "threat_type": "phishing",
  "risk_score": 95,
  "action": "block",
  "reason": "Urgency combined with a suspicious link indicates phishing."
}

## Tech Stack
	•	Gemini 3 API – AI reasoning engine
	•	FastAPI – Backend API
	•	Next.js – Frontend UI
	•	Google Cloud Run – Scalable deployment
	•	Python & TypeScript
	•	Hybrid Deterministic + AI Architecture

## Use Cases
	•	Chat & email security for users
	•	Trust & Safety systems for platforms
	•	AI prompt-injection defense
	•	Cybersecurity education and awareness
## Contributors

- **Pamala Madhumitha Yadav**
- **Munisai Kannemmagari**
- **Sankeesa Anshu**
- **Amith Reddy Karre**
  
## License

MIT License
