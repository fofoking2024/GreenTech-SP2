import os
import json

# Simple stub for AI analysis – replace with real API integration later.

def analyze_device_issue(description: str, language: str = "en"):
    """Return a short summary and a JSON string of the (mock) conversation.
    In a production setting, this would call an LLM service (e.g., OpenAI, Anthropic).
    """
    # Mock summary generation
    summary = f"Analyzed issue: {description[:100]}..." if description else "No description provided."
    # Mock full conversation – here just the user description
    conversation = [{"role": "user", "content": description}]
    conversation_json = json.dumps(conversation, ensure_ascii=False)
    return summary, conversation_json
