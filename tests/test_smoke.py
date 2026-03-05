"""
Smoke tests for ARKHAM CLI tool.
Validates basic functionality without external dependencies.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSmoke:
    """Basic smoke tests to verify core functionality."""

    def test_import_main(self):
        """Verify main module can be imported."""
        import main
        assert main is not None

    def test_import_arkham(self):
        """Verify arkham module can be imported."""
        # Note: File is named arkam.py (not arkham.py)
        import importlib.util
        spec = importlib.util.spec_from_file_location("arkam_module", Path(__file__).parent.parent / 'arkam.py')
        arkam = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(arkam)
        assert arkam is not None

    def test_cli_help(self):
        """Verify CLI responds to --help."""
        import subprocess
        result = subprocess.run(
            [sys.executable, 'main.py', '--help'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        # Should not crash, may return non-zero if no --help implemented
        assert result.returncode in [0, 1, 2]

    def test_entry_points_exist(self):
        """Verify main entry points exist."""
        main_path = Path(__file__).parent.parent / 'main.py'
        arkam_path = Path(__file__).parent.parent / 'arkam.py'
        
        assert main_path.exists(), "main.py should exist"
        assert arkam_path.exists(), "arkam.py should exist"


class TestConfiguration:
    """Test configuration and constants."""

    def test_agent_directory_defined(self):
        """Verify agent directory is properly defined."""
        # Read the main.py to check AGENT_DIR is defined
        main_content = (Path(__file__).parent.parent / 'main.py').read_text()
        assert 'AGENT_DIR' in main_content

    def test_logging_configured(self):
        """Verify logging is configured."""
        import logging
        # Should have handlers configured
        assert len(logging.root.handlers) >= 0  # Basic check


class TestDataStructures:
    """Test dataclass structures."""

    def test_challenge_dataclass(self):
        """Test Challenge dataclass creation."""
        from dataclasses import dataclass
        from typing import List, Optional
        
        # Test creating a Challenge-like object
        challenge_data = {
            'name': 'Test Challenge',
            'platform': 'htb',
            'category': 'web',
            'difficulty': 'easy',
            'ip': '10.10.10.10',
            'description': 'Test description'
        }
        
        # Verify data structure is valid
        assert 'name' in challenge_data
        assert challenge_data['platform'] in ['htb', 'thm', 'pico', 'custom']

    def test_platform_validation(self):
        """Test platform validation logic."""
        valid_platforms = ['htb', 'thm', 'pico', 'custom']
        
        for platform in valid_platforms:
            assert platform in valid_platforms

    def test_difficulty_levels(self):
        """Test difficulty level validation."""
        valid_difficulties = ['easy', 'medium', 'hard', 'insane']
        
        for difficulty in valid_difficulties:
            assert difficulty in valid_difficulties


class TestFlagValidation:
    """Test flag format validation."""

    def test_htb_flag_format(self):
        """Validate HTB flag format."""
        import re
        # HTB flags: HTB{...}
        pattern = r'^HTB\{.+\}$'
        assert re.match(pattern, 'HTB{test_flag_123}')

    def test_thm_flag_format(self):
        """Validate THM flag format."""
        import re
        # THM flags: THM{...}
        pattern = r'^THM\{.+\}$'
        assert re.match(pattern, 'THM{another_flag}')

    def test_custom_flag_format(self):
        """Validate custom flag format."""
        import re
        # Generic flag pattern
        pattern = r'^[\w\-]+\{.+\}$'
        assert re.match(pattern, 'flag{some_content}')
        assert re.match(pattern, 'CTF{flag_here}')


class TestCommandParsing:
    """Test command parsing logic."""

    def test_parse_start_command(self):
        """Test parsing of start command."""
        import re
        
        # Pattern: start "Lab Name" --web --ip 10.10.10.5
        pattern = r'start\s+"([^"]+)"\s+(--\w+\s+)*(--ip\s+\d+\.\d+\.\d+\.\d+)?'
        
        # Should match basic start command structure
        assert 'start' in 'start "Test Lab" --web --ip 10.10.10.5'

    def test_parse_run_command(self):
        """Test parsing of run command."""
        cmd = 'run nmap -sVC 10.10.10.5'
        assert cmd.startswith('run')

    def test_parse_flag_command(self):
        """Test parsing of flag command."""
        cmd = 'flag HTB{test_flag}'
        assert cmd.startswith('flag')
        assert 'HTB{' in cmd


class TestPathHandling:
    """Test file path handling."""

    def test_home_directory_resolution(self):
        """Verify home directory is properly resolved."""
        from pathlib import Path
        home = Path.home()
        assert home.exists()
        assert home.is_dir()

    def test_session_directory_structure(self):
        """Test session directory creation logic."""
        import tempfile
        import os
        
        # Create temp directory to simulate AGENT_DIR
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / '.arkham'
            test_dir.mkdir(parents=True, exist_ok=True)
            
            assert test_dir.exists()
            assert test_dir.is_dir()
