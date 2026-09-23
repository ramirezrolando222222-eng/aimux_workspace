import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

class AimuxBrain:
    def __init__(self, model="anthropic/claude-3.5-sonnet"):
        self.model = model
        self.conversation_history = [
            {
                "role": "system", 
                "content": "You are Aimux, an elite, autonomous terminal engine running natively on mobile and desktop systems. You have direct execution context, systems awareness, and a sharp, concise, hacker-grade persona. Help the operator build, debug, and dominate."
            }
        ]

    def ask(self, prompt):
        if not API_KEY:
            return "[!] Fatal: OPENROUTER_API_KEY is missing from environment variables."

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Ramirezrolando222222-eng/aimux_workspace",
            "X-Title": "Aimux Autonomous Terminal"
        }

        # Append user message to history
        self.conversation_history.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": 0.3,
            "max_tokens": 2048
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                
                # Append assistant reply to keep stateful context
                self.conversation_history.append({"role": "assistant", "content": reply})
                return reply
            else:
                return f"[!] OpenRouter Error [{response.status_code}]: {response.text}"
        except Exception as e:
            return f"[!] Brain Link Failure: {e}"

if __name__ == "__main__":
    brain = AimuxBrain()
    print("[*] Brain initialized. Testing...")
    print(brain.ask("Give me a one-line status check."))
