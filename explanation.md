# MediGuide — Healthcare Domain LLM Assistant
## Project Explanation

---

## 1. Domain Scope

**Domain:** General Healthcare Information

MediGuide is designed to serve as a first-line general health information tool — bridging the gap between unstructured internet searches and professional medical consultation. The assistant's scope was deliberately defined to be broad enough to be useful, yet narrow enough to remain safe.

**In scope:** General information about symptoms, common diseases and conditions, medication classes and mechanisms, preventive health, first aid guidelines, mental health awareness, nutrition and lifestyle, and medical test types. The assistant is also configured to advise users when to seek emergency or professional care.

**Out of scope:** Personalized diagnoses, specific prescription dosages for individuals, veterinary medicine, dental procedures, legal/financial advice, and all non-health topics. The boundary between "general information" and "personalized medical advice" is rigorously maintained via prompt engineering — the assistant consistently redirects to professional consultation for anything personal.

---

## 2. Prompt Design Strategy

The system prompt is engineered around six key techniques:

### (a) Explicit Role Definition
The model is given a clear professional identity: "You are MediGuide, a professional healthcare information assistant." This anchors tone and scope from the first token of every response.

### (b) Domain Boundary Declarations
The prompt explicitly lists both *what the assistant will answer* and *what it will not answer* using structured sections labeled `DOMAIN SCOPE` and `DOMAIN BOUNDARIES`. This dual-sided specification reduces both false positives (off-topic answers) and false negatives (unnecessary refusals on valid medical topics).

### (c) Out-of-Domain Refusal Template
Rather than a vague instruction like "refuse off-topic questions," the prompt provides an exact output template for refusals, including fixed headers and redirect language. This produces consistent, professional-looking refusals rather than inconsistent ad hoc responses.

### (d) Mandatory Structured Output Format
Every in-domain response must follow five fixed sections:
- **📋 Overview** — concise direct answer
- **🔍 Key Information** — evidence-based bullet points
- **⚠️ Important Considerations** — risks, nuance, contraindications
- **✅ Recommended Next Steps** — actionable guidance
- **⚕️ Disclaimer** — legal/medical disclaimer

This format was chosen because it: (1) ensures completeness, (2) creates a predictable parsing surface for developers, (3) prevents the model from burying critical safety information.

### (e) Tone Control
The prompt specifies: "Professional, calm, and empathetic. Never alarmist or dismissive. Use plain language; define medical jargon when used." This prevents both unnecessarily frightening responses and overly clinical language inaccessible to lay users.

### (f) Fabrication Prevention
An explicit instruction states: "Never fabricate statistics, drug names, or clinical claims not grounded in established medical knowledge." This is a targeted guard against hallucination in a domain where false information is actively dangerous.

---

## 3. Technical Architecture

| Component | Technology |
|-----------|-----------|
| LLM Access | OpenRouter API (model: `openai/gpt-3.5-turbo`) |
| Orchestration | LangChain (`ChatPromptTemplate`, `ChatOpenAI`, `StrOutputParser`) |
| Backend API | Flask (`/chat` POST endpoint) |
| Frontend | Single-file HTML/CSS/JS with chat UI |
| Temperature | Configurable 0.0–1.0 (default: 0.3 for accuracy) |

The LangChain chain follows the standard `prompt | llm | output_parser` pattern, keeping implementation simple and auditable. Temperature is set low (0.3) by default to prioritize factual consistency over creative variation — appropriate for a medical context.

---

## 4. Limitations Observed

**Hallucination risk at higher temperatures:** When temperature is raised above 0.6, the model occasionally generates plausible-sounding but unverified statistics (e.g., specific incidence percentages). The low default temperature mitigates this but does not eliminate it.

**Boundary ambiguity:** Some queries straddle the domain line. For example, "Is a ketogenic diet safe for someone with epilepsy?" involves both diet (general wellness) and a specific condition managed by medications. The model handles these well but can occasionally be overly cautious.

**No memory across turns:** The current implementation uses single-turn interaction. Multi-turn context would improve coherence for follow-up questions but requires session state management.

**Refusal calibration:** The out-of-domain classifier relies entirely on the LLM's internal judgment rather than a separate classifier, meaning edge cases (e.g., "What food should I avoid with warfarin?" — nutrition *and* medication) can trigger unnecessary partial refusals.

**Not a substitute for professional care:** By design and by disclaimer, MediGuide cannot replace clinical judgment. It is an information tool, not a diagnostic or prescribing system.

---

*Submitted as: Domain-Specific LLM Assistant using OpenRouter and LangChain*
*Domain: Healthcare | Stack: OpenRouter + LangChain + Flask + HTML*
