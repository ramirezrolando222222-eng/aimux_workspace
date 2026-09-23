import os
import sys
import subprocess
import shutil
from dotenv import load_dotenv
from aimux_openrouter_brain import AimuxBrain

load_dotenv()

def detect_platform():
    if os.path.exists("/data/data/com.termux"):
        return "android_termux"
    elif sys.platform.startswith("linux"):
        return "linux_desktop"
    return "desktop"

def get_system_telemetry():
    total, used, free = shutil.disk_usage(os.path.expanduser("~/aimux_workspace"))
    disk_free_gb = free // (2**30)
    db_status = "ONLINE (Port 5432)" if os.path.exists("/data/data/com.termux/files/usr/var/lib/postgresql") else "LOCAL/STANDBY"
    ai_status = "LOADED (Claude 3.5 Sonnet)" if os.getenv("OPENROUTER_API_KEY") else "MISSING KEY"
    return disk_free_gb, db_status, ai_status

def print_hud(platform):
    disk_free, db_status, ai_status = get_system_telemetry()
    print("=" * 65)
    print("  [AIMUX COMMAND CENTER] - Autonomous Terminal & AI Grid")
    print("=" * 65)
    print(f"  » Platform Environment : {platform.upper()}")
    print(f"  » AI Brain (OpenRouter): {ai_status}")
    print(f"  » Local Database Engine: {db_status}")
    print(f"  » Workspace Disk Free  : {disk_free} GB")
    print(f"  » Hardware Protection  : WakeLock Active")
    print("=" * 65)
    print("  Commands:")
    print("    • 'mode term'  -> Switch to Native Terminal Mode")
    print("    • 'mode ai'    -> Switch to Autonomous AI Brain Mode")
    print("    • 'exit'       -> Shut down Aimux")
    print("=" * 65 + "\n")

def main():
    platform = detect_platform()
    if platform == "android_termux":
        try:
            from platforms.android_termux import AimuxTermux
            AimuxTermux.wake_lock()
        except ImportError:
            pass

    print_hud(platform)
    
    # Initialize the stateful AI brain instance
    brain = AimuxBrain()
    current_mode = "term"

    while True:
        try:
            prompt_symbol = "aimux[term]⚡> " if current_mode == "term" else "aimux[ai-brain]🤖> "
            user_input = input(prompt_symbol).strip()
            
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("[*] Shutting down Aimux. Stay dangerous.")
                break
            
            if user_input.lower() == "mode term":
                current_mode = "term"
                print("[*] Switched to Native Terminal Mode.")
                continue
            elif user_input.lower() == "mode ai":
                current_mode = "ai"
                print("[*] Switched to Autonomous AI Brain Mode. Context active.")
                continue

            if current_mode == "ai":
                print("\n[AI Brain is thinking...]")
                answer = brain.ask(user_input)
                print(f"\n{answer}\n")
            else:
                result = subprocess.run(user_input, shell=True, text=True, capture_output=True)
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, end="")

        except KeyboardInterrupt:
            print("\n[!] Use 'exit' to quit properly.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
