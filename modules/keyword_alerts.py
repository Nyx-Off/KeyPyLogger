"""
Keyword Alerts Module
Educational implementation of keyword-based monitoring and alerting
"""

import re
from datetime import datetime
from collections import deque


class KeywordAlertSystem:
    """
    Monitors text for specific keywords and triggers alerts
    Educational purpose: Demonstrates targeted surveillance and pattern matching
    """

    def __init__(self, keywords, alert_callback, case_sensitive=False, use_regex=False):
        """
        Initialize keyword alert system

        Args:
            keywords (list): List of keywords or regex patterns to monitor
            alert_callback (function): Function to call when keyword detected
                                       Signature: callback(keyword, context, timestamp)
            case_sensitive (bool): Whether matching should be case-sensitive
            use_regex (bool): Whether to treat keywords as regex patterns
        """
        self.keywords = keywords if keywords else []
        self.alert_callback = alert_callback
        self.case_sensitive = case_sensitive
        self.use_regex = use_regex
        self.buffer = deque(maxlen=500)  # Keep last 500 characters for context
        self.triggered_keywords = {}  # Track keyword detections
        self.compile_patterns()

    def compile_patterns(self):
        """Compile regex patterns for efficient matching"""
        self.patterns = []

        for keyword in self.keywords:
            try:
                if self.use_regex:
                    # User provided regex
                    pattern = re.compile(
                        keyword,
                        flags=0 if self.case_sensitive else re.IGNORECASE
                    )
                else:
                    # Escape special chars and create word boundary pattern
                    escaped = re.escape(keyword)
                    pattern = re.compile(
                        r'\b' + escaped + r'\b',
                        flags=0 if self.case_sensitive else re.IGNORECASE
                    )

                self.patterns.append((keyword, pattern))

            except re.error as e:
                print(f"[!] Invalid keyword pattern '{keyword}': {e}")

    def add_keyword(self, keyword):
        """Add a new keyword to monitor"""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
            self.compile_patterns()

    def remove_keyword(self, keyword):
        """Remove a keyword from monitoring"""
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self.compile_patterns()

    def process_text(self, text):
        """
        Process text and check for keyword matches

        Args:
            text (str): Text to analyze

        Returns:
            list: List of (keyword, match_position) tuples for detected keywords
        """
        # Add to buffer for context
        self.buffer.extend(text)

        detected = []

        # Check each pattern
        for keyword, pattern in self.patterns:
            matches = pattern.finditer(text)

            for match in matches:
                # Get context (text around the match)
                buffer_str = ''.join(self.buffer)
                match_pos = len(buffer_str) - len(text) + match.start()

                # Extract context (50 chars before and after)
                context_start = max(0, match_pos - 50)
                context_end = min(len(buffer_str), match_pos + len(match.group()) + 50)
                context = buffer_str[context_start:context_end]

                # Trigger alert
                timestamp = datetime.now()
                self.alert_callback(keyword, match.group(), context, timestamp)

                # Track detection
                if keyword not in self.triggered_keywords:
                    self.triggered_keywords[keyword] = []

                self.triggered_keywords[keyword].append({
                    'timestamp': timestamp,
                    'matched_text': match.group(),
                    'context': context
                })

                detected.append((keyword, match.group()))

        return detected

    def get_statistics(self):
        """Get detection statistics"""
        stats = {
            'total_keywords': len(self.keywords),
            'triggered_keywords': len(self.triggered_keywords),
            'total_detections': sum(len(v) for v in self.triggered_keywords.values()),
            'detections_by_keyword': {
                k: len(v) for k, v in self.triggered_keywords.items()
            }
        }
        return stats

    def reset_statistics(self):
        """Reset detection statistics"""
        self.triggered_keywords = {}

    def get_recent_detections(self, limit=10):
        """Get most recent detections across all keywords"""
        all_detections = []

        for keyword, detections in self.triggered_keywords.items():
            for detection in detections:
                all_detections.append({
                    'keyword': keyword,
                    **detection
                })

        # Sort by timestamp (most recent first)
        all_detections.sort(key=lambda x: x['timestamp'], reverse=True)

        return all_detections[:limit]


class PresetKeywordLists:
    """Predefined keyword lists for common monitoring scenarios"""

    @staticmethod
    def get_credentials():
        """Keywords related to credentials and authentication"""
        return [
            'password', 'passwd', 'pwd',
            'username', 'user', 'login',
            'email', 'mail',
            'secret', 'token', 'api',
            'key', 'credential',
            'authentication', 'auth'
        ]

    @staticmethod
    def get_financial():
        """Keywords related to financial information"""
        return [
            'credit card', 'debit card',
            'card number', 'cvv', 'cvc',
            'bank account', 'account number',
            'routing number', 'swift',
            'iban', 'paypal',
            'bitcoin', 'crypto', 'wallet'
        ]

    @staticmethod
    def get_personal_info():
        """Keywords related to personal information"""
        return [
            'ssn', 'social security',
            'date of birth', 'dob',
            'address', 'phone number',
            'passport', 'driver license',
            'insurance', 'medical'
        ]

    @staticmethod
    def get_corporate():
        """Keywords related to corporate/business information"""
        return [
            'confidential', 'classified',
            'internal only', 'proprietary',
            'trade secret', 'nda',
            'contract', 'agreement',
            'merger', 'acquisition'
        ]

    @staticmethod
    def get_technical():
        """Keywords related to technical information"""
        return [
            'database', 'db', 'sql',
            'server', 'admin', 'root',
            'localhost', '127.0.0.1',
            'connection string', 'config',
            'backup', 'restore'
        ]

    @staticmethod
    def get_all_presets():
        """Get all preset categories"""
        return {
            'credentials': PresetKeywordLists.get_credentials(),
            'financial': PresetKeywordLists.get_financial(),
            'personal_info': PresetKeywordLists.get_personal_info(),
            'corporate': PresetKeywordLists.get_corporate(),
            'technical': PresetKeywordLists.get_technical()
        }
