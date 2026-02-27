"""
Flask API server for MediGuide Healthcare Assistant
Exposes POST /chat endpoint for the frontend UI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from assistant import ask_mediguide, build_chain
import os

app = Flask(__name__)
CORS(app)

# Build chain once at startup
chain = None


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "MediGuide Healthcare Assistant"})


@app.route("/chat", methods=["POST"])
def chat():
    global chain
    
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    query = data["query"].strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    temperature = float(data.get("temperature", 0.3))
    
    try:
        if chain is None:
            chain = build_chain()
        
        response = ask_mediguide(query, chain)
        return jsonify({
            "query": query,
            "response": response,
            "model": "openai/gpt-3.5-turbo via OpenRouter"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting MediGuide API server on http://localhost:5000")
    app.run(debug=True, port=5000)
