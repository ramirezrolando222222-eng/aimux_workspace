import urllib.request
import json

class LocalAimuxBrain:
    def __init__(self, host="http://127.0.0.1:11434", model="llama3.2"):
        self.host = host
        self.model = model
        self.url = f"{self.host}/api/generate"

    def think(self, prompt):
        """Send prompt to the local on-device AI runtime completely offline."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "[!] Empty response from local model.")
        except Exception as e:
            return f"[!] Local Inference Engine Offline or Unreachable: {e}. Ensure local service is running."

if __name__ == "__main__":
    brain = LocalAimuxBrain()
    print("[*] Testing local offline brain connection...")
    print(brain.think("System status check."))
