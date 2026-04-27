"""
ARKHAM - Main agent class for CTF operations.
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from pathlib import Path

from .models import Challenge, Command
from .tools import CTFTools
from .platforms import HackTheBox, TryHackMe
from .solvers import ChallengeSolver

logger = logging.getLogger(__name__)

# Configuration
AGENT_DIR = Path.home() / ".arkham"
SESSION_DIR = AGENT_DIR / "sessions"
LOGS_DIR = AGENT_DIR / "logs"
HISTORY_FILE = AGENT_DIR / "history.json"


class CTFAgent:
    """Agente principal para CTFs."""
    
    def __init__(self, platform: str = "custom"):
        self.platform = platform
        self.current_challenge: Optional[Challenge] = None
        self.tools = CTFTools()
        self.solvers = ChallengeSolver()
        self.session_data: Dict = {}
        
        # Initialize platforms
        self.htb = HackTheBox()
        self.thm = TryHackMe()
        
        # Ensure directories exist
        self._init_directories()
        
        # Load history
        self.history = self._load_history()
    
    def _init_directories(self) -> None:
        """Initialize required directories."""
        for d in [AGENT_DIR, SESSION_DIR, LOGS_DIR]:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_history(self) -> Dict:
        """Carga historial de sesiones."""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Corrupted history file, creating new one")
        return {"sessions": [], "challenges": [], "flags": []}
    
    def _save_history(self) -> None:
        """Guarda historial."""
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def start_challenge(self, name: str, category: str = "misc", 
                       difficulty: str = "medium", ip: str = None, 
                       port: int = None, description: str = "") -> Challenge:
        """Inicia un nuevo desafío."""
        self.current_challenge = Challenge(
            name=name,
            platform=self.platform,
            category=category,
            difficulty=difficulty,
            ip=ip,
            port=port,
            description=description
        )
        
        logger.info(f"🎯 Started challenge: {name} ({category})")
        return self.current_challenge
    
    def run_command(self, command: str, category: str = "general", 
                   notes: str = "") -> str:
        """Ejecuta un comando y lo registra."""
        logger.info(f"$ {command}")
        
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=300
            )
            
            cmd_record = Command(
                command=command,
                output=result.stdout + result.stderr,
                timestamp=datetime.now().isoformat(),
                category=category,
                success=result.returncode == 0,
                notes=notes
            )
            
            if self.current_challenge:
                self.current_challenge.commands_used.append(asdict(cmd_record))
            
            return result.stdout + result.stderr
            
        except subprocess.TimeoutExpired:
            error_msg = "[TIMEOUT: Command took too long]"
            logger.warning(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"[ERROR: {e}]"
            logger.error(error_msg)
            return error_msg
    
    def add_tool(self, tool_name: str) -> None:
        """Registra uso de una herramienta."""
        if self.current_challenge and tool_name not in self.current_challenge.tools_used:
            self.current_challenge.tools_used.append(tool_name)
    
    def add_flag(self, flag: str, notes: str = "") -> None:
        """Registra una flag encontrada."""
        if not self.current_challenge:
            logger.warning("No active challenge")
            return
        
        self.current_challenge.flags_found.append(flag)
        
        # Save to history
        self.history["flags"].append({
            "flag": flag,
            "challenge": self.current_challenge.name,
            "platform": self.platform,
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        })
        self._save_history()
        
        logger.info(f"🚩 FLAG FOUND: {flag}")
    
    def add_note(self, note: str) -> None:
        """Agrega una nota al desafío actual."""
        if self.current_challenge:
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.current_challenge.notes += f"\n[{timestamp}] {note}"
    
    def suggest_next(self) -> List[str]:
        """Sugiere próximos pasos basándose en el contexto."""
        if not self.current_challenge:
            return ["Start a challenge first: start <name>"]
        
        suggestions = []
        category = self.current_challenge.category
        
        if category == "web":
            suggestions = [
                "Run gobuster: gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt",
                "Check nikto: nikto -h <target>",
                "Look for forms and parameters",
                "Try SQLMap if parameters found"
            ]
        elif category == "pwn":
            suggestions = [
                "Run checksec: checksec --file=<binary>",
                "Analyze with ghidra or radare2",
                "Look for buffer overflows"
            ]
        elif category == "rev":
            suggestions = [
                "Run strings: strings <binary> | grep flag",
                "Use ghidra for decompilation",
                "Check for packed binaries"
            ]
        elif category == "crypto":
            suggestions = [
                "Try base64 decode",
                "Check for Caesar cipher",
                "Use cyberchef: https://gchq.github.io/CyberChef/"
            ]
        elif category == "osint":
            suggestions = [
                "Search username on social media",
                "Check for email leaks",
                "Use Sherlock: python3 sherlock.py <username>"
            ]
        else:
            suggestions = [
                "Run nmap scan: nmap -sVC <target>",
                "Look for low-hanging fruit",
                "Check source code if web"
            ]
        
        return suggestions
    
    def generate_report(self) -> str:
        """Genera reporte del desafío actual."""
        if not self.current_challenge:
            return "No active challenge"
        
        c = self.current_challenge
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    CTF CHALLENGE REPORT                         ║
╠══════════════════════════════════════════════════════════════════╣
║ Name:        {c.name:<50} ║
║ Platform:    {c.platform:<50} ║
║ Category:    {c.category:<50} ║
║ Difficulty:  {c.difficulty:<50} ║
║ IP:          {c.ip or 'N/A':<50} ║
╚══════════════════════════════════════════════════════════════════╝

📝 DESCRIPTION:
{c.description}

🚩 FLAGS FOUND ({len(c.flags_found)}):
{chr(10).join(f"  - {f}" for f in c.flags_found) if c.flags_found else "  None yet"}

🛠️ TOOLS USED:
{chr(10).join(f"  - {t}" for t in c.tools_used) if c.tools_used else "  None"}

📋 COMMANDS EXECUTED ({len(c.commands_used)}):
"""
        for cmd in c.commands_used[-10:]:  # Last 10
            status = "✓" if cmd["success"] else "✗"
            report += f"  [{status}] {cmd['timestamp'][11:19]} {cmd['category']}: {cmd['command'][:40]}...\n"
        
        report += f"""
📝 NOTES:
{c.notes if c.notes else "  No notes"}
"""
        
        return report
    
    def save_session(self, session_name: str = None) -> Optional[Path]:
        """Guarda la sesión actual."""
        if not self.current_challenge:
            return None
        
        if not session_name:
            session_name = f"{self.current_challenge.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session_file = SESSION_DIR / f"{session_name}.json"
        
        try:
            with open(session_file, "w") as f:
                json.dump(asdict(self.current_challenge), f, indent=2)
            
            # Also save to history
            self.history["challenges"].append(asdict(self.current_challenge))
            self._save_history()
            
            logger.info(f"💾 Session saved: {session_file}")
            return session_file
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return None
    
    def list_sessions(self) -> List[str]:
        """Lista sesiones guardadas."""
        try:
            return [f.name for f in SESSION_DIR.glob("*.json")]
        except Exception:
            return []
    
    def load_session(self, session_name: str) -> str:
        """Carga una sesión previa."""
        session_file = SESSION_DIR / f"{session_name}.json"
        
        if not session_file.exists():
            return f"Session not found: {session_name}"
        
        try:
            with open(session_file) as f:
                data = json.load(f)
                self.current_challenge = Challenge(**data)
            
            logger.info(f"📂 Loaded session: {session_name}")
            return f"Loaded: {self.current_challenge.name}"
            
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return f"Error loading session: {e}"
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas."""
        return {
            "total_flags": len(self.history.get("flags", [])),
            "total_challenges": len(self.history.get("challenges", [])),
            "sessions_saved": len(self.list_sessions()),
            "platform": self.platform,
            "categories": list(set([c.get("category") for c in self.history.get("challenges", []) if c]))
        }
