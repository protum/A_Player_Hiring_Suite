"""
Local server launcher for A-Player Hiring Suite.

This script starts the FastAPI backend and optionally opens the browser.
"""

import uvicorn
import webbrowser
import time
import threading
import sys


def open_browser():
    """Open browser after short delay."""
    time.sleep(2)
    webbrowser.open("http://localhost:8000")
    print("\n✓ Browser opened at http://localhost:8000")


def main():
    """Run the application."""
    print("=" * 60)
    print("A-Player Hiring Suite")
    print("Local Evidence-Based Hiring & Leadership Assessment Platform")
    print("=" * 60)
    print("\nStarting server...")

    # Open browser in background thread
    if "--no-browser" not in sys.argv:
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()

    # Start server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
