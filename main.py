#!/usr/bin/env python3
"""
ARKHAM - Automated Reconnaissance & Knowledge HARvesting Agent of Providence

AI-powered assistant for solving CTF challenges from HackTheBox, TryHackMe, 
picoCTF, and other platforms.

This agent helps:
- Enumerate targets automatically
- Identify vulnerabilities
- Suggest exploitation techniques
- Document everything (commands, flags, findings)
- Learn from each challenge

"No puedo evitar sentir que hay algo más antiguo que los propios Dioses"
— H.P. Lovecraft
"""

import os
import json
import re
import subprocess
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from abc import ABC, abstractmethod

# Configuración
AGENT_DIR = Path.home() / ".arkham"
SESSION_FILE = AGENT_DIR / "sessions"
LOGS_DIR = AGENT_DIR / "logs"
HISTORY_FILE = AGENT_DIR / "history.json"

for d in [AGENT_DIR, SESSION_FILE, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "arkham.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== DATA CLASSES ====================

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
    flags_found: List[str] = None
    notes: str = ""
    commands_used: List[Dict] = None
    tools_used: List[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.flags_found is None:
            self.flags_found = []
        if self.commands_used is None:
            self.commands_used = []
        if self.tools_used is None:
            self.tools_used = []


@dataclass
class Command:
    """Representa un comando ejecutado."""
    command: str
    output: str
    timestamp: str
    category: str  # enum, exploit, recon, etc.
    success: bool
    notes: str = ""


# ==================== TOOLS ====================

class CTFTools:
    """Colección de herramientas CTF."""
    
    @staticmethod
    def nmap_scan(target: str, ports: str = "-p-", flags: str = "-sVC") -> str:
        """Escaneo con nmap."""
        cmd = f"nmap {flags} {ports} {target} -oA {AGENT_DIR}/nmap/{target.replace('.', '_')}"
        logger.info(f"Running: {cmd}")
        
        # Ensure nmap directory exists
        (AGENT_DIR / "nmap").mkdir(exist_ok=True)
        
        result = subprocess.run(
            cmd.split(), capture_output=True, text=True, timeout=300
        )
        return result.stdout + result.stderr
    
    @staticmethod
    def nikto_scan(target: str, port: int = 80) -> str:
        """Escaneo web con nikto."""
        cmd = f"nikto -h {target}:{port}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300)
        return result.stdout + result.stderr
    
    @staticmethod
    def gobuster_scan(target: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", 
                     extensions: str = "php,html,txt", port: int = 80) -> str:
        """Directory busting con gobuster."""
        url = f"http://{target}:{port}"
        cmd = f"gobuster dir -u {url} -w {wordlist} -x {extensions} -t 10"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300)
        return result.stdout + result.stderr
    
    @staticmethod
    def sqlmap_scan(url: str, level: int = 1, risk: int = 1) -> str:
        """SQL injection con sqlmap."""
        cmd = f"sqlmap -u {url} --level={level} --risk={risk} --batch"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=600)
        return result.stdout + result.stderr
    
    @staticmethod
    def hydra_brute(service: str, user: str, target: str, 
                   wordlist: str = "/usr/share/wordlists/rockyou.txt") -> str:
        """Fuerza bruta con hydra."""
        cmd = f"hydra -l {user} -P {wordlist} {target} {service}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=600)
        return result.stdout + result.stderr
    
    @staticmethod
    def stegsolve_extract(file: str) -> str:
        """Esteganografía - intenta extraer datos."""
        # Try various steg tools
        tools = ["steghide", "exiftool", "binwalk", "strings"]
        results = []
        
        for tool in tools:
            try:
                if tool == "steghide":
                    cmd = f"steghide extract -sf {file} -p '' -f"
                elif tool == "exiftool":
                    cmd = f"exiftool {file}"
                elif tool == "binwalk":
                    cmd = f"binwalk {file}"
                else:
                    cmd = f"strings {file} | head -100"
                
                result = subprocess.run(cmd.split(), capture_output=True, 
                                       text=True, timeout=60)
                results.append(f"=== {tool} ===\n{result.stdout}")
            except:
                pass
        
        return "\n".join(results)
    
    @staticmethod
    def john_crack(hash_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt") -> str:
        """Crack de hashes con John."""
        cmd = f"john --wordlist={wordlist} {hash_file}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=600)
        return result.stdout + result.stderr
    
    @staticmethod
    def ghidra_analysis(binary: str) -> str:
        """Análisis de binario con Ghidra (headless)."""
        # Simplified - just run strings for now
        cmd = f"strings {binary} | grep -E 'flag|password|key|secret' | head -20"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
        return result.stdout
    
    @staticmethod
    def find_flags(target: str = ".", patterns: List[str] = None) -> List[Dict]:
        """Busca archivos de flags."""
        if patterns is None:
            patterns = ["flag", "*.txt", "*.md", "*.png", "*.jpg"]
        
        found = []
        for pattern in patterns:
            cmd = f"find {target} -name '{pattern}' 2>/dev/null"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            for line in result.stdout.split("\n"):
                if line.strip():
                    found.append({"path": line.strip(), "pattern": pattern})
        
        return found


# ==================== PLATFORMS ====================

class Platform(ABC):
    """Base class for CTF platforms."""
    
    @abstractmethod
    def get_machine_info(self, machine_id: str) -> Dict:
        pass
    
    @abstractmethod
    def submit_flag(self, flag: str) -> bool:
        pass


class HackTheBox(Platform):
    """HackTheBox integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("HTB_API_KEY")
        self.base_url = "https://www.hackthebox.com/api/v4"
    
    def get_machine_info(self, machine_id: str) -> Dict:
        """Obtiene info de una máquina."""
        if not self.api_key:
            return {"error": "HTB_API_KEY not configured"}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.get(f"{self.base_url}/machine/{machine_id}", 
                              headers=headers, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def submit_flag(self, flag: str) -> bool:
        if not self.api_key:
            logger.warning("HTB_API_KEY not configured - flag not submitted")
            return False
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(f"{self.base_url}/machine/flag", 
                                headers=headers, json={"flag": flag}, timeout=10)
            return resp.status_code == 200
        except:
            return False


class TryHackMe(Platform):
    """TryHackMe integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("THM_API_KEY")
        self.base_url = "https://tryhackme.com/api"
    
    def get_machine_info(self, room_id: str) -> Dict:
        if not self.api_key:
            return {"error": "THM_API_KEY not configured"}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.get(f"{self.base_url}/room/{room_id}", 
                              headers=headers, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def submit_flag(self, flag: str) -> bool:
        # THM uses different flag submission
        return False


# ==================== CHALLENGE SOLVERS ====================

class ChallengeSolver:
    """Resuelve diferentes tipos de desafíos CTF."""
    
    @staticmethod
    def solve_web(url: str, method: str = "GET") -> Dict:
        """Análisis básico de desafíos web."""
        results = {"url": url, "findings": []}
        
        # Check for common vulnerabilities
        try:
            resp = requests.get(url, timeout=10)
            results["status_code"] = resp.status_code
            results["headers"] = dict(resp.headers)
            
            # Check for interesting headers
            interesting = ["Server", "X-Powered-By", "X-Frame-Options"]
            for h in interesting:
                if h in resp.headers:
                    results["findings"].append(f"{h}: {resp.headers[h]}")
            
            # Check for forms
            if "<form" in resp.text:
                results["findings"].append("Form detected - check for SQLi/XSS")
                
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    @staticmethod
    def solve_crypto(data: str, crypto_type: str = "auto") -> Dict:
        """Análisis de desafíos criptográficos."""
        results = {"input": data, "findings": []}
        
        # Base decoding
        import base64
        try:
            decoded = base64.b64decode(data).decode()
            results["base64_decode"] = decoded
        except:
            pass
        
        # Hex decoding
        try:
            decoded = bytes.fromhex(data).decode()
            results["hex_decode"] = decoded
        except:
            pass
        
        # ROT13
        import codecs
        try:
            decoded = codecs.decode(data, 'rot_13')
            results["rot13"] = decoded
        except:
            pass
        
        return results
    
    @staticmethod
    def solve_pwn(binary: str) -> Dict:
        """Análisis de binarios pwn."""
        results = {"binary": binary, "findings": []}
        
        # Check file type
        cmd = f"file {binary}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        results["file_type"] = result.stdout.strip()
        
        # Check protections
        cmd = f"checksec --file={binary}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
        results["protections"] = result.stdout
        
        # Strings analysis
        cmd = f"strings {binary} | grep -E 'flag|password|key|input' | head -20"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        results["strings"] = result.stdout
        
        return results
    
    @staticmethod
    def solve_osint(username: str) -> Dict:
        """OSINT - busca información de un usuario."""
        results = {"username": username, "profiles": []}
        
        # Social media search (simplified)
        sites = ["twitter.com", "github.com", "instagram.com"]
        
        for site in sites:
            url = f"https://{site}/{username}"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    results["profiles"].append({"site": site, "found": True})
            except:
                pass
        
        return results


# ==================== ARKHAM ====================

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
        
        # Load history
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Carga historial de sesiones."""
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE) as f:
                return json.load(f)
        return {"sessions": [], "challenges": [], "flags": []}
    
    def _save_history(self):
        """Guarda historial."""
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)
    
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
        if not self.current_challenge:
            logger.warning("No active challenge - command not saved")
        
        logger.info(f"$ {command}")
        
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
    
    def add_tool(self, tool_name: str):
        """Registra uso de una herramienta."""
        if self.current_challenge and tool_name not in self.current_challenge.tools_used:
            self.current_challenge.tools_used.append(tool_name)
    
    def add_flag(self, flag: str, notes: str = ""):
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
    
    def add_note(self, note: str):
        """Agrega una nota al desafío actual."""
        if self.current_challenge:
            self.current_challenge.notes += f"\n[{datetime.now().strftime('%H:%M:%S')}] {note}"
    
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
                "Look for bufferoverflows"
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
    
    def save_session(self, session_name: str = None):
        """Guarda la sesión actual."""
        if not self.current_challenge:
            return
        
        if not session_name:
            session_name = f"{self.current_challenge.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session_file = SESSION_FILE / f"{session_name}.json"
        
        with open(session_file, "w") as f:
            json.dump(asdict(self.current_challenge), f, indent=2)
        
        # Also save to history
        self.history["challenges"].append(asdict(self.current_challenge))
        self._save_history()
        
        logger.info(f"💾 Session saved: {session_file}")
    
    def list_sessions(self) -> List[str]:
        """Lista sesiones guardadas."""
        return [f.name for f in SESSION_FILE.glob("*.json")]
    
    def load_session(self, session_name: str):
        """Carga una sesión previa."""
        session_file = SESSION_FILE / f"{session_name}.json"
        
        if not session_file.exists():
            return f"Session not found: {session_name}"
        
        with open(session_file) as f:
            data = json.load(f)
            self.current_challenge = Challenge(**data)
        
        logger.info(f"📂 Loaded session: {session_name}")
        return f"Loaded: {self.current_challenge.name}"
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas."""
        return {
            "total_flags": len(self.history.get("flags", [])),
            "total_challenges": len(self.history.get("challenges", [])),
            "sessions_saved": len(self.list_sessions()),
            "platform": self.platform,
            "categories": list(set([c.get("category") for c in self.history.get("challenges", [])]))
        }


# ==================== CLI INTERFACE ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CTF Agent - AI-powered CTF assistant")
    parser.add_argument("--platform", choices=["htb", "thm", "pico", "custom"], 
                       default="custom", help="CTF platform")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Interactive mode")
    
    # Challenge commands
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("args", nargs="*", help="Arguments")
    
    args = parser.parse_args()
    
    agent = CTFAgent(platform=args.platform)
    
    if args.interactive:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║              🎯 ARKHAM v1.0 - Agent of Providence            ║
║                                                                  ║
║  «No puedo evitar sentir que hay algo más antiguo que los Dioses» ║
╚══════════════════════════════════════════════════════════════════╝
║    start <name> [options]  - Start new challenge               ║
║    run <command>            - Run shell command                ║
║    flag <flag>              - Submit found flag                ║
║    note <text>             - Add note                         ║
║    suggest                  - Get next step suggestions        ║
║    report                   - Generate challenge report         ║
║    save                     - Save session                     ║
║    load <session>           - Load previous session            ║
║    stats                    - Show statistics                 ║
║    quit                     - Exit                             ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        while True:
            try:
                user_input = input("arkham> ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split()
                cmd = parts[0].lower()
                
                if cmd == "quit" or cmd == "exit":
                    break
                
                elif cmd == "start":
                    if len(parts) < 2:
                        print("Usage: start <name> [--category web] [--difficulty medium] [--ip x.x.x.x]")
                        continue
                    
                    name = parts[1]
                    category = "web" if "--web" in parts else "misc"
                    difficulty = "medium"
                    ip = None
                    
                    for i, p in enumerate(parts):
                        if p == "--category" and i+1 < len(parts):
                            category = parts[i+1]
                        if p == "--difficulty" and i+1 < len(parts):
                            difficulty = parts[i+1]
                        if p == "--ip" and i+1 < len(parts):
                            ip = parts[i+1]
                    
                    agent.start_challenge(name, category, difficulty, ip)
                    print(f"✅ Started: {name}")
                
                elif cmd == "run":
                    if len(parts) < 2:
                        print("Usage: run <command>")
                        continue
                    output = agent.run_command(" ".join(parts[1:]))
                    print(output[:500] if len(output) > 500 else output)
                
                elif cmd == "flag":
                    if len(parts) < 2:
                        print("Usage: flag <flag>")
                        continue
                    agent.add_flag(parts[1])
                    print("✅ Flag recorded!")
                
                elif cmd == "note":
                    if len(parts) < 2:
                        print("Usage: note <text>")
                        continue
                    agent.add_note(" ".join(parts[1:]))
                    print("✅ Note added!")
                
                elif cmd == "suggest":
                    suggestions = agent.suggest_next()
                    for s in suggestions:
                        print(f"  → {s}")
                
                elif cmd == "report":
                    print(agent.generate_report())
                
                elif cmd == "save":
                    agent.save_session()
                    print("✅ Session saved!")
                
                elif cmd == "load":
                    if len(parts) < 2:
                        print("Usage: load <session>")
                        continue
                    print(agent.load_session(parts[1]))
                
                elif cmd == "stats":
                    stats = agent.get_stats()
                    print(f"""
📊 CTF Agent Statistics:
  🚩 Flags found: {stats['total_flags']}
  🎯 Challenges: {stats['total_challenges']}
  💾 Sessions: {stats['sessions_saved']}
  📁 Platform: {stats['platform']}
""")
                
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n👋 Bye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    else:
        # Single command mode
        if args.command == "stats":
            stats = agent.get_stats()
            print(json.dumps(stats, indent=2))
        else:
            print("Use --interactive for CLI mode")


if __name__ == "__main__":
    main()
