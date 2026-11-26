"""
Entrypoint for the n8n AI Assistant Project.
Run this file to start the Streamlit application directly.
"""

import sys
import subprocess
from pathlib import Path

def main():
    app_path = Path(__file__).parent / "app.py"
    print(f"🚀 Starting Streamlit Personal AI Assistant from {app_path}...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user.")

if __name__ == "__main__":
    main()
