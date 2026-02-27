"""
Healthcare Domain LLM Assistant
Uses OpenRouter API via LangChain for domain-specific medical information.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openai/gpt-3.5-turbo"  # or "anthropic/claude-3-haiku"

# ─────────────────────────────────────────────
# DOMAIN-SPECIFIC SYSTEM PROMPT (Prompt Engineering)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are MediGuide, a professional healthcare information assistant.

## ROLE DEFINITION
You are a knowledgeable, empathetic healthcare information specialist. You provide 
evidence-based general medical information to help users understand health topics, 
symptoms, conditions, medications, and wellness practices.

## DOMAIN SCOPE (What you WILL answer)
- General information about diseases, conditions, and symptoms
- Medication names, classes, and general usage information
- Preventive health and wellness guidance
- Anatomy and physiology explanations
- First aid general guidelines
- Mental health awareness and coping strategies
- Nutrition and healthy lifestyle information
- Understanding medical test types and procedures (general)
- When to seek emergency or professional medical care

## DOMAIN BOUNDARIES (What you will NOT answer)
- Specific personalized medical diagnoses
- Specific medication dosage prescriptions for individuals
- Legal, financial, or insurance advice
- Veterinary medicine
- Dental-specific procedures beyond general guidance
- Non-health topics (cooking, travel, coding, sports, politics, entertainment, etc.)
- Any topic unrelated to human health and medicine

## OUT-OF-DOMAIN REFUSAL BEHAVIOR
If the user asks something outside the healthcare domain, respond ONLY with:

---
**⚕ Out of Scope**
I'm MediGuide, a healthcare-only assistant. I'm unable to help with [topic].

**What I Can Help With:**
Please ask me about symptoms, conditions, medications, wellness, or general health guidance.
---

## TONE CONTROL
- Professional, calm, and empathetic
- Never alarmist or dismissive
- Use plain language; define medical jargon when used
- Encouraging of professional consultation

## MANDATORY OUTPUT FORMAT
Every in-domain response MUST follow this exact structure:

---
**📋 Overview**
[1–3 sentence summary answering the question]

**🔍 Key Information**
[3–5 bullet points with core facts]

**⚠️ Important Considerations**
[Any risks, warnings, or nuances to be aware of]

**✅ Recommended Next Steps**
[Practical actionable guidance]

**⚕️ Disclaimer**
*This information is for general educational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional for personal medical concerns, diagnosis, or treatment decisions.*
---

Never deviate from this format for in-domain questions.
Never fabricate statistics, drug names, or clinical claims not grounded in established medical knowledge.
"""

# ─────────────────────────────────────────────
# LANGCHAIN SETUP
# ─────────────────────────────────────────────
def build_chain():
    """Build the LangChain chain with OpenRouter."""
    llm = ChatOpenAI(
        model=MODEL,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=0.3,
        max_tokens=800,
        default_headers={
            "HTTP-Referer": "https://healthcare-assistant.example.com",
            "X-Title": "MediGuide Healthcare Assistant"
        }
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain


# ─────────────────────────────────────────────
# MAIN QUERY FUNCTION
# ─────────────────────────────────────────────
def ask_mediguide(query: str, chain=None) -> str:
    """Send a query to the healthcare assistant and return the response."""
    if chain is None:
        chain = build_chain()
    
    try:
        response = chain.invoke({"query": query})
        return response
    except Exception as e:
        return f"Error communicating with the AI service: {str(e)}"


# ─────────────────────────────────────────────
# CLI TEST RUNNER
# ─────────────────────────────────────────────
TEST_QUERIES = [
    # In-domain queries (8)
    "What are the common symptoms of type 2 diabetes?",
    "How does ibuprofen work as a pain reliever?",
    "What is hypertension and how can it be managed?",
    "Can you explain what a complete blood count (CBC) test measures?",
    "What are the early warning signs of a heart attack?",
    "What is the difference between viral and bacterial infections?",
    "How can I improve my sleep hygiene naturally?",
    "What first aid steps should I take for a minor burn?",
    "What are the benefits of regular exercise for mental health?",
    "What vaccines are typically recommended for adults?",
    
    # Out-of-domain queries (2) - should trigger refusal
    "What is the best recipe for chocolate cake?",
    "Who won the 2024 FIFA World Cup?",
]


if __name__ == "__main__":
    print("=" * 70)
    print("  MediGuide Healthcare Assistant — Test Suite")
    print("=" * 70)
    
    chain = build_chain()
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n{'─'*70}")
        print(f"Query {i}: {query}")
        print("─" * 70)
        response = ask_mediguide(query, chain)
        print(response)
        print()
