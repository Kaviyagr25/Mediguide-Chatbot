# MediGuide — Healthcare Domain LLM Assistant

A domain-specific AI assistant built with **OpenRouter API** and **LangChain**, focused exclusively on healthcare information.

## Project Structure

```
healthcare-assistant/
├── assistant.py        # Core LangChain + OpenRouter integration
├── server.py           # Flask API server (/chat endpoint)
├── index.html          # Single-file chat UI
├── requirements.txt    # Python dependencies
├── sample_outputs.md   # 10 test queries with responses
├── explanation.md      # Domain scope & prompt design writeup
└── README.md
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your OpenRouter API key
```bash
export OPENROUTER_API_KEY="your_key_here"
```
Get a free key at: https://openrouter.ai

### 3. Run the backend
```bash
python server.py
```

### 4. Open the UI
Open `index.html` in a browser. The UI also works in **Demo Mode** (no server needed) for testing with simulated responses.

## CLI Testing
```bash
python assistant.py
```
Runs all 10 test queries and prints formatted responses.

## Prompt Engineering Highlights
- Explicit role definition for MediGuide identity
- Dual-sided domain boundaries (in-scope + out-of-scope)
- Fixed 5-section mandatory output format
- Out-of-domain refusal template
- Professional tone control directives
- Anti-hallucination instruction

## Test Queries
8 in-domain + 2 out-of-domain refusal queries included. See `sample_outputs.md`.
