import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO", "Ramirezrolando222222-eng/aimux_workspace")

class AimuxGitHub:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

    def check_status(self):
        """Check repository status via Git subprocess"""
        result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True)
        print("[*] Local Git Status:\n" + result.stdout)

    def quick_sync(self, commit_message="chore: auto-sync via Aimux GitHub plugin"):
        """Stage, commit, and push changes safely"""
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "master"], check=True)
            print("[+] Successfully synced changes to GitHub!")
        except subprocess.CalledProcessError as e:
            print(f"[!] Sync failed: {e}")

if __name__ == "__main__":
    gh = AimuxGitHub()
    gh.check_status()
