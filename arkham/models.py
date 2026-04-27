"""
Models for ARKHAM - Data classes and structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class Challenge:
    """Representa un desafío CTF."""
    name: str
    platform: str  # htb, thm, pico, custom
    category: str  # web, pwn, crypto, rev, osint, misc
    difficulty: str  # easy, medium, hard, insane
    ip: Optional[str] = None
    port: Optional[int] = None
    description: str = ""
    flags_found: List[str] = field(default_factory=list)
    notes: str = ""
    commands_used: List[Dict[str, Any]] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Command:
    """Representa un comando ejecutado."""
    command: str
    output: str
    timestamp: str
    category: str  # enum, exploit, recon, etc.
    success: bool
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
