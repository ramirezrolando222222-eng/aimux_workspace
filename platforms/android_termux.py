import subprocess
import os

class AimuxTermux:
    @staticmethod
    def wake_lock():
        """Acquire a Termux WakeLock to prevent Android from sleeping the session."""
        try:
            subprocess.run(["termux-wake-lock"], check=True)
            print("[+] Termux WakeLock acquired. Background processes (PostgreSQL/Sync) are protected.")
        except FileNotFoundError:
            print("[!] termux-api package not found. Install it via 'pkg install termux-api' for hardware integration.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to acquire WakeLock: {e}")

    @staticmethod
    def wake_unlock():
        """Release the Termux WakeLock."""
        try:
            subprocess.run(["termux-wake-unlock"], check=True)
            print("[-] Termux WakeLock released.")
        except Exception as e:
            print(f"[!] Error releasing WakeLock: {e}")

    @staticmethod
    def notify(title, message):
        """Trigger a native Android notification via Termux API."""
        try:
            subprocess.run(["termux-notification", "-t", title, "-c", message], check=True)
        except Exception:
            # Fallback if notification API isn't installed
            pass

if __name__ == "__main__":
    print("[*] Initializing Aimux Termux Power Engine...")
    AimuxTermux.wake_lock()
