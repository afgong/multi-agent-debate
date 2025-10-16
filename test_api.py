"""Test Anthropic API connection and model availability."""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key present: {bool(api_key)}")
print(f"API Key starts with: {api_key[:10] if api_key else 'None'}...")

client = Anthropic(api_key=api_key)

# Try different model names
models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
]

for model in models_to_try:
    try:
        print(f"\nTrying model: {model}")
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✓ SUCCESS! Model {model} works!")
        print(f"Response: {response.content[0].text}")
        break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:100]}")
