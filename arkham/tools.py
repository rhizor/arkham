"""
CTFTools module - Security tools wrapper for CTF operations.
"""

import subprocess
import logging
from typing import Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)


class CTFTools:
    """Colección de herramientas CTF con wrappers seguros."""
    
    @staticmethod
    def _run_command(cmd: str, timeout: int = 300) -> str:
        """Ejecuta un comando de forma segura."""
        try:
            result = subprocess.run(
                cmd.split(), 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            logger.warning(f"Command timed out after {timeout}s: {cmd}")
            return f"[TIMEOUT after {timeout}s]"
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return f"[ERROR: {e}]"
    
    @staticmethod
    def nmap_scan(target: str, ports: str = "-p-", flags: str = "-sVC", output_dir: Path = None) -> str:
        """Escaneo con nmap."""
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"nmap_{target.replace('.', '_')}"
            cmd = f"nmap {flags} {ports} {target} -oA {output_file}"
        else:
            cmd = f"nmap {flags} {ports} {target}"
        
        logger.info(f"Running nmap scan on {target}")
        return CTFTools._run_command(cmd, timeout=300)
    
    @staticmethod
    def nikto_scan(target: str, port: int = 80) -> str:
        """Escaneo web con nikto."""
        cmd = f"nikto -h {target}:{port}"
        return CTFTools._run_command(cmd, timeout=300)
    
    @staticmethod
    def gobuster_scan(target: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", 
                     extensions: str = "php,html,txt", port: int = 80) -> str:
        """Directory busting con gobuster."""
        url = f"http://{target}:{port}"
        cmd = f"gobuster dir -u {url} -w {wordlist} -x {extensions} -t 10"
        return CTFTools._run_command(cmd, timeout=300)
    
    @staticmethod
    def sqlmap_scan(url: str, level: int = 1, risk: int = 1) -> str:
        """SQL injection con sqlmap."""
        cmd = f"sqlmap -u {url} --level={level} --risk={risk} --batch"
        return CTFTools._run_command(cmd, timeout=600)
    
    @staticmethod
    def hydra_brute(service: str, user: str, target: str, 
                   wordlist: str = "/usr/share/wordlists/rockyou.txt") -> str:
        """Fuerza bruta con hydra."""
        cmd = f"hydra -l {user} -P {wordlist} {target} {service}"
        return CTFTools._run_command(cmd, timeout=600)
    
    @staticmethod
    def stegsolve_extract(file: str) -> str:
        """Esteganografía - intenta extraer datos."""
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
                else:  # strings
                    cmd = f"strings {file}"
                
                result = subprocess.run(cmd.split(), capture_output=True, 
                                       text=True, timeout=60)
                if result.stdout:
                    results.append(f"=== {tool} ===\n{result.stdout[:500]}")
            except Exception:
                pass
        
        return "\n".join(results) if results else "No data extracted"
    
    @staticmethod
    def john_crack(hash_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt") -> str:
        """Crack de hashes con John."""
        cmd = f"john --wordlist={wordlist} {hash_file}"
        return CTFTools._run_command(cmd, timeout=600)
    
    @staticmethod
    def ghidra_analysis(binary: str) -> str:
        """Análisis de binario con Ghidra (simplified)."""
        cmd = f"strings {binary}"
        return CTFTools._run_command(cmd, timeout=60)
    
    @staticmethod
    def find_flags(target: str = ".", patterns: List[str] = None) -> List[Dict[str, str]]:
        """Busca archivos potenciales de flags."""
        if patterns is None:
            patterns = ["flag*", "*.txt", "*.md", "*.png", "*.jpg"]
        
        found = []
        for pattern in patterns:
            cmd = f"find {target} -name '{pattern}' -type f 2>/dev/null"
            try:
                result = subprocess.run(cmd.split(), capture_output=True, 
                                       text=True, timeout=30)
                for line in result.stdout.split("\n"):
                    if line.strip():
                        found.append({"path": line.strip(), "pattern": pattern})
            except Exception:
                pass
        
        return found
