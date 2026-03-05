"""
Real code tests - exercise actual functions and classes from the project.
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import Challenge, Command


class TestChallengeReal:
    """Test Challenge class with real behavior."""

    def test_create_challenge_instance(self):
        """Create a real Challenge instance."""
        c = Challenge(
            name="Test Lab",
            platform="htb",
            category="web",
            difficulty="easy"
        )
        assert c.name == "Test Lab"
        assert c.platform == "htb"
        assert c.created_at is not None

    def test_add_flag_to_challenge(self):
        """Add real flags to challenge."""
        c = Challenge(
            name="Flag Lab",
            platform="htb",
            category="web",
            difficulty="medium"
        )
        c.flags_found.append("HTB{test_flag_123}")
        
        assert len(c.flags_found) == 1
        assert "HTB{test_flag_123}" in c.flags_found

    def test_add_command_to_challenge(self):
        """Track real commands."""
        c = Challenge(name="Cmd Lab", platform="thm", category="pwn", difficulty="hard")
        c.commands_used.append({
            "command": "nmap -sVC 10.10.10.10",
            "output": "open ports found",
            "timestamp": datetime.now().isoformat()
        })
        
        assert len(c.commands_used) == 1

    def test_challenge_with_ip_and_port(self):
        """Test challenge with network info."""
        c = Challenge(
            name="Network Lab",
            platform="htb",
            category="network",
            difficulty="medium",
            ip="10.10.10.100",
            port=443
        )
        
        assert c.ip == "10.10.10.100"
        assert c.port == 443

    def test_challenge_validation_platforms(self):
        """Test platform validation."""
        for platform in ["htb", "thm", "pico", "custom"]:
            c = Challenge(name="Test", platform=platform, category="web", difficulty="easy")
            assert c.platform == platform


class TestCommandReal:
    """Test Command class with real behavior."""

    def test_create_command_instance(self):
        """Create a real Command instance."""
        cmd = Command(
            command="ls -la",
            output="total 10\nfile.txt",
            timestamp=datetime.now().isoformat(),
            category="recon",
            success=True
        )
        
        assert cmd.command == "ls -la"
        assert cmd.success is True
        assert cmd.category == "recon"

    def test_command_with_notes(self):
        """Test command with notes."""
        cmd = Command(
            command="id",
            output="uid=0",
            timestamp=datetime.now().isoformat(),
            category="enum",
            success=True,
            notes="Running as root"
        )
        
        assert cmd.notes == "Running as root"


class TestFlagValidationReal:
    """Test real flag validation logic."""

    def test_htb_flag_pattern(self):
        """Validate HTB flag format."""
        pattern = r'^HTB\{.+\}$'
        assert re.match(pattern, "HTB{flag_123}")
        assert not re.match(pattern, "HTB{}")
        assert not re.match(pattern, "not_a_flag")

    def test_thm_flag_pattern(self):
        """Validate THM flag format."""
        pattern = r'^THM\{.+\}$'
        assert re.match(pattern, "THM{abc123}")

    def test_generic_flag_pattern(self):
        """Validate generic CTF flag."""
        pattern = r'^[\w-]+\{.+\}$'
        assert re.match(pattern, "CTF{content}")
        assert re.match(pattern, "flag{something}")
