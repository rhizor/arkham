"""
Smoke tests - verify core modules can be imported.
"""

import sys
from pathlib import Path

def test_import_main_module():
    """Import the real main module."""
    import main
    assert main is not None

def test_import_arkam_module():
    """Import the real arkham module."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("arkam", Path(__file__).parent.parent / 'arkam.py')
    arkham = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arkham)
    assert arkham is not None

def test_challenge_class_exists():
    """Verify Challenge class exists in main."""
    import main
    assert hasattr(main, 'Challenge')

def test_command_class_exists():
    """Verify Command class exists in main."""
    import main
    assert hasattr(main, 'Command')

def test_ctf_tools_class_exists():
    """Verify CTFTools class exists in main."""
    import main
    assert hasattr(main, 'CTFTools')
