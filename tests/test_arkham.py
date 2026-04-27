"""
Test suite for ARKHAM CTF Agent.
"""

import pytest
import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from arkham.models import Challenge, Command
from arkham.tools import CTFTools
from arkham.platforms import HackTheBox, TryHackMe
from arkham.solvers import ChallengeSolver


class TestModels:
    """Tests for data models."""
    
    def test_challenge_creation(self):
        """Test Challenge dataclass creation."""
        challenge = Challenge(
            name="Test Challenge",
            platform="htb",
            category="web",
            difficulty="medium",
            ip="10.10.10.10"
        )
        
        assert challenge.name == "Test Challenge"
        assert challenge.platform == "htb"
        assert challenge.category == "web"
        assert challenge.difficulty == "medium"
        assert challenge.ip == "10.10.10.10"
        assert challenge.flags_found == []
        assert challenge.tools_used == []
        assert challenge.created_at is not None
    
    def test_command_creation(self):
        """Test Command dataclass creation."""
        cmd = Command(
            command="nmap -sV localhost",
            output="Starting Nmap",
            timestamp=datetime.now().isoformat(),
            category="recon",
            success=True,
            notes="Test note"
        )
        
        assert cmd.command == "nmap -sV localhost"
        assert cmd.success is True
        assert cmd.category == "recon"


class TestCTFTools:
    """Tests for CTF Tools."""
    
    def test_tools_exist(self):
        """Verify tools module is importable."""
        assert hasattr(CTFTools, 'nmap_scan')
        assert hasattr(CTFTools, 'gobuster_scan')
        assert hasattr(CTFTools, 'sqlmap_scan')
    
    def test_find_flags_with_no_matches(self):
        """Test find_flags with no matching files."""
        # This should return empty list when run in temp dir with no files
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = CTFTools.find_flags(tmpdir, patterns=["*.flag"])
            assert result == []


class TestPlatforms:
    """Tests for platform integrations."""
    
    def test_htb_no_api_key(self):
        """Test HTB without API key."""
        import os
        # Ensure no API key is set
        if "HTB_API_KEY" in os.environ:
            del os.environ["HTB_API_KEY"]
        
        htb = HackTheBox()
        result = htb.get_machine_info("test-machine")
        assert "error" in result
        assert "HTB_API_KEY not configured" in result["error"]
    
    def test_thm_no_api_key(self):
        """Test THM without API key."""
        import os
        if "THM_API_KEY" in os.environ:
            del os.environ["THM_API_KEY"]
        
        thm = TryHackMe()
        result = thm.get_machine_info("test-room")
        assert "error" in result
        assert "THM_API_KEY not configured" in result["error"]


class TestSolvers:
    """Tests for challenge solvers."""
    
    def test_solve_crypto_base64(self):
        """Test crypto solver with base64."""
        encoded = "SGVsbG8gV29ybGQh"  # "Hello World!"
        result = ChallengeSolver.solve_crypto(encoded)
        
        assert "decoded" in result
        assert "base64" in result["decoded"]
        assert result["decoded"]["base64"] == "Hello World!"
    
    def test_solve_crypto_rot13(self):
        """Test crypto solver with ROT13."""
        encoded = "Uryyb Jbeyq!"  # "Hello World!" in ROT13
        result = ChallengeSolver.solve_crypto(encoded)
        
        assert "decoded" in result
        assert "rot13" in result["decoded"]
        assert "Hello World!" in result["findings"][0]


class TestIntegration:
    """Integration tests."""
    
    def test_package_import(self):
        """Test that the package can be imported correctly."""
        import arkham
        
        assert hasattr(arkham, 'CTFAgent')
        assert hasattr(arkham, 'CTFTools')
        assert hasattr(arkham, 'Challenge')
        assert hasattr(arkham, '__version__')
        assert arkham.__version__ == "1.0.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
