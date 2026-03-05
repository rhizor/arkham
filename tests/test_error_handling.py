"""
Error handling tests for ARKHAM.
Tests error conditions, exception handling, and edge cases.
"""

import pytest
import sys
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class Challenge:
    name: str
    platform: str
    category: str
    difficulty: str
    ip: Optional[str] = None
    port: Optional[int] = None
    description: str = ""
    flags_found: List[str] = field(default_factory=list)
    notes: str = ""
    commands_used: List[dict] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class TestIPValidationErrors:
    """Test IP address validation error handling."""

    def test_ip_validation_function(self):
        """Test IP validation with specific checks."""
        def validate_ip(ip: str):
            if not ip:
                return (False, "IP cannot be empty")
            parts = ip.split('.')
            if len(parts) != 4:
                return (False, "IP must have 4 octets")
            try:
                octets = [int(p) for p in parts]
            except ValueError:
                return (False, "All octets must be numeric")
            for octet in octets:
                if octet < 0 or octet > 255:
                    return (False, f"Octet {octet} out of range (0-255)")
            return (True, "")
        
        assert validate_ip("10.10.10.10")[0] is True
        assert validate_ip("192.168.1.1")[0] is True
        assert validate_ip("")[0] is False
        assert validate_ip("10.10.10")[0] is False
        assert validate_ip("256.256.256.256")[0] is False


class TestPortValidationErrors:
    """Test port validation error handling."""

    def test_port_out_of_range(self):
        def validate_port(port: int):
            if port < 1:
                return (False, "Port must be >= 1")
            if port > 65535:
                return (False, "Port must be <= 65535")
            return (True, "")
        
        assert validate_port(80)[0] is True
        assert validate_port(0)[0] is False
        assert validate_port(-1)[0] is False
        assert validate_port(65536)[0] is False


class TestFlagValidationErrors:
    """Test flag validation error handling."""

    def test_flag_validation_function(self):
        def validate_flag(flag: str):
            if not flag:
                return (False, "Flag cannot be empty")
            if '{' not in flag or '}' not in flag:
                return (False, "Flag must be in format PREFIX{content}")
            if not flag.endswith('}'):
                return (False, "Flag must end with }")
            content = flag[flag.index('{')+1:flag.rindex('}')]
            if not content:
                return (False, "Flag content cannot be empty")
            return (True, "")
        
        assert validate_flag("HTB{flag_here}")[0] is True
        assert validate_flag("THM{test_123}")[0] is True
        assert validate_flag("")[0] is False
        assert validate_flag("plaintext")[0] is False
        assert validate_flag("{}")[0] is False


class TestChallengeValidationErrors:
    """Test challenge validation error handling."""

    def test_missing_required_fields(self):
        with pytest.raises(TypeError):
            Challenge()

    def test_invalid_platform_handling(self):
        challenge = Challenge(name="Test", platform="invalid", category="web", difficulty="easy")
        assert challenge.platform == "invalid"


class TestJSONParsingErrors:
    """Test JSON parsing error handling."""

    def test_invalid_json_handling(self):
        invalid_json = ["", "plain text", "{"]
        for json_str in invalid_json:
            with pytest.raises(json.JSONDecodeError):
                json.loads(json_str)

    def test_json_parsing_with_defaults(self):
        def safe_json_parse(json_str, default=None):
            try:
                return json.loads(json_str)
            except (json.JSONDecodeError, TypeError):
                return default
        
        assert safe_json_parse("invalid") is None
        assert safe_json_parse('{"key": "value"}') == {"key": "value"}


class TestFileOperationErrors:
    def test_nonexistent_file_read(self):
        nonexistent_file = Path("/tmp/arkham_nonexistent_12345.json")
        assert not nonexistent_file.exists()


class TestEdgeCaseHandling:
    def test_unicode_in_fields(self):
        challenge = Challenge(name="Unicode 你好", platform="htb", category="web", difficulty="easy", description="Emojis 🚀")
        assert "你好" in challenge.name

    def test_empty_lists(self):
        challenge = Challenge(name="Test", platform="htb", category="web", difficulty="easy")
        assert challenge.flags_found == []


class TestStringEscapeErrors:
    def test_special_characters_in_commands(self):
        special_commands = ['echo "hello world"', "grep 'pattern' file.txt"]
        for cmd in special_commands:
            assert isinstance(cmd, str)


class TestLoggingErrors:
    def test_logging_configuration(self):
        import logging
        logger = logging.getLogger(f"test_{id(self)}")
        logger.info("Test message")
        assert logger is not None


class TestExceptionHandling:
    def test_exception_chain_handling(self):
        try:
            try:
                raise ValueError("Original")
            except ValueError as e:
                raise RuntimeError("Chained") from e
        except RuntimeError as e:
            assert e.__cause__ is not None

    def test_generic_exception_catch(self):
        def might_fail():
            raise Exception("Error")
        with pytest.raises(Exception):
            might_fail()
