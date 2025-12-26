"""
Watchdog Module - Auto-restart and health monitoring
Educational implementation of process monitoring and auto-recovery
"""

import os
import sys
import time
import subprocess
import threading
import psutil
from pathlib import Path


class WatchdogManager:
    """
    Monitors the main process and restarts it if it crashes
    Educational purpose: Demonstrates malware resilience techniques
    """

    def __init__(self, target_script, check_interval=30, max_restarts=10):
        """
        Initialize watchdog manager

        Args:
            target_script (str): Path to the script to monitor
            check_interval (int): Seconds between health checks
            max_restarts (int): Maximum restart attempts before giving up
        """
        self.target_script = os.path.abspath(target_script)
        self.check_interval = check_interval
        self.max_restarts = max_restarts
        self.restart_count = 0
        self.process = None
        self.running = False
        self.monitor_thread = None

    def start_watchdog(self):
        """Start the watchdog in a separate thread"""
        if self.running:
            return False

        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=False)
        self.monitor_thread.start()
        return True

    def stop_watchdog(self):
        """Stop the watchdog"""
        self.running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running and self.restart_count < self.max_restarts:
            try:
                # Start the process if not running
                if self.process is None or self.process.poll() is not None:
                    if self.restart_count > 0:
                        print(f"[*] Watchdog: Restarting process (attempt {self.restart_count}/{self.max_restarts})")

                    self._start_target()
                    self.restart_count += 1

                # Wait before next check
                time.sleep(self.check_interval)

            except Exception as e:
                print(f"[!] Watchdog error: {e}")
                time.sleep(self.check_interval)

        if self.restart_count >= self.max_restarts:
            print(f"[!] Watchdog: Max restart attempts ({self.max_restarts}) reached. Giving up.")

    def _start_target(self):
        """Start the target script"""
        try:
            # Use subprocess to start the target script
            if sys.platform == 'win32':
                # Windows: start detached
                self.process = subprocess.Popen(
                    [sys.executable, self.target_script],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Linux/Unix: start detached
                self.process = subprocess.Popen(
                    [sys.executable, self.target_script],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            print(f"[*] Watchdog: Started process (PID: {self.process.pid})")

        except Exception as e:
            print(f"[!] Watchdog: Failed to start process: {e}")
            self.process = None


class ProcessMonitor:
    """
    Monitors process health and system resources
    """

    def __init__(self, process_name=None):
        """
        Initialize process monitor

        Args:
            process_name (str): Name of process to monitor (default: current process)
        """
        self.process_name = process_name or Path(sys.argv[0]).name
        self.start_time = time.time()

    def is_process_running(self, process_name=None):
        """Check if a process is running"""
        name = process_name or self.process_name

        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == name:
                    return True, proc.pid
        except:
            pass

        return False, None

    def get_process_count(self, process_name=None):
        """Count how many instances of a process are running"""
        name = process_name or self.process_name
        count = 0

        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == name:
                    count += 1
        except:
            pass

        return count

    def get_health_info(self):
        """Get current process health information"""
        try:
            process = psutil.Process(os.getpid())

            info = {
                'pid': process.pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_mb': process.memory_info().rss / 1024 / 1024,
                'num_threads': process.num_threads(),
                'uptime_seconds': time.time() - self.start_time,
                'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 'N/A'
            }

            return info

        except Exception as e:
            return {'error': str(e)}

    def ensure_single_instance(self):
        """
        Ensure only one instance is running
        Returns: (is_unique, existing_pid)
        """
        count = self.get_process_count()

        if count > 1:
            # Find the other instance
            current_pid = os.getpid()

            try:
                for proc in psutil.process_iter(['name', 'pid']):
                    if proc.info['name'] == self.process_name and proc.info['pid'] != current_pid:
                        return False, proc.info['pid']
            except:
                pass

            return False, None

        return True, None

    @staticmethod
    def kill_process_by_name(process_name):
        """Kill all processes with given name"""
        killed = []

        try:
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] == process_name:
                    try:
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        killed.append(proc.info['pid'])
                    except:
                        pass
        except:
            pass

        return killed

    @staticmethod
    def kill_process_by_pid(pid):
        """Kill a specific process by PID"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except:
            return False


class HealthChecker:
    """
    Periodic health checking with callback
    """

    def __init__(self, callback, check_interval=60):
        """
        Initialize health checker

        Args:
            callback (function): Function to call with health info
                                 Signature: callback(health_info)
            check_interval (int): Seconds between health checks
        """
        self.callback = callback
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.monitor = ProcessMonitor()

    def start(self):
        """Start periodic health checks"""
        if self.running:
            return False

        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """Stop health checks"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _check_loop(self):
        """Main checking loop"""
        while self.running:
            try:
                health_info = self.monitor.get_health_info()
                self.callback(health_info)
            except Exception as e:
                print(f"[!] Health check error: {e}")

            # Wait for interval
            for _ in range(self.check_interval):
                if not self.running:
                    break
                time.sleep(1)
