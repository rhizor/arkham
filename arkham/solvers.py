"""
Challenge solvers for different CTF categories.
"""

import subprocess
import base64
import codecs
import logging
from typing import Dict

import requests

logger = logging.getLogger(__name__)


class ChallengeSolver:
    """Resuelve diferentes tipos de desafíos CTF."""
    
    @staticmethod
    def solve_web(url: str, method: str = "GET") -> Dict:
        """Análisis básico de desafíos web."""
        results = {"url": url, "findings": [], "headers": {}}
        
        try:
            if method.upper() == "GET":
                resp = requests.get(url, timeout=10)
            else:
                resp = requests.post(url, timeout=10)
            
            results["status_code"] = resp.status_code
            results["headers"] = dict(resp.headers)
            
            # Check for interesting headers
            interesting = ["Server", "X-Powered-By", "X-Frame-Options", "X-Content-Type-Options"]
            for h in interesting:
                if h in resp.headers:
                    results["findings"].append(f"{h}: {resp.headers[h]}")
            
            # Check for forms
            if "<form" in resp.text:
                results["findings"].append("Form detected - check for SQLi/XSS")
            
            # Check for potential flags in response
            if "flag{" in resp.text.lower() or "ctf{" in resp.text.lower():
                results["findings"].append("Possible flag detected in response")
                
        except requests.exceptions.RequestException as e:
            results["error"] = str(e)
            logger.error(f"Web check failed: {e}")
        
        return results
    
    @staticmethod
    def solve_crypto(data: str) -> Dict:
        """Análisis de desafíos criptográficos."""
        results = {"input": data, "findings": [], "decoded": {}}
        
        # Base64 decoding
        try:
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            results["decoded"]["base64"] = decoded
            results["findings"].append(f"Base64 decoded: {decoded[:100]}")
        except Exception:
            pass
        
        # Hex decoding
        try:
            decoded = bytes.fromhex(data).decode('utf-8', errors='ignore')
            results["decoded"]["hex"] = decoded
            results["findings"].append(f"Hex decoded: {decoded[:100]}")
        except Exception:
            pass
        
        # ROT13
        try:
            decoded = codecs.decode(data, 'rot_13')
            results["decoded"]["rot13"] = decoded
            results["findings"].append(f"ROT13: {decoded[:100]}")
        except Exception:
            pass
        
        return results
    
    @staticmethod
    def solve_pwn(binary: str) -> Dict:
        """Análisis de binarios pwn."""
        results = {"binary": binary, "findings": [], "protections": {}}
        
        # Check file type
        try:
            cmd = f"file {binary}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            results["file_type"] = result.stdout.strip()
        except Exception as e:
            logger.error(f"File check failed: {e}")
        
        # Check protections
        try:
            cmd = f"checksec --file={binary}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            results["protections_text"] = result.stdout
        except Exception:
            results["protections_text"] = "checksec not available"
        
        # Strings analysis
        try:
            cmd = f"strings {binary}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            interesting = ["flag", "password", "key", "secret", "win", "shell"]
            for line in result.stdout.split("\n"):
                if any(k in line.lower() for k in interesting):
                    results["findings"].append(f"String: {line}")
        except Exception as e:
            logger.error(f"Strings analysis failed: {e}")
        
        return results
    
    @staticmethod
    def solve_osint(username: str) -> Dict:
        """OSINT - busca información de un usuario."""
        results = {"username": username, "profiles": [], "suggestions": []}
        
        # Social media search
        sites = [
            ("twitter.com", f"https://twitter.com/{username}"),
            ("github.com", f"https://github.com/{username}"),
            ("instagram.com", f"https://instagram.com/{username}"),
        ]
        
        for site, url in sites:
            try:
                resp = requests.get(url, timeout=5, allow_redirects=False)
                if resp.status_code == 200:
                    results["profiles"].append({"site": site, "url": url, "found": True})
            except requests.exceptions.RequestException:
                pass
        
        results["suggestions"] = [
            f"Check: https://github.com/{username}",
            f"Check: https://twitter.com/{username}",
            f"Use Sherlock: python3 sherlock {username}",
        ]
        
        return results
    
    @staticmethod
    def solve_rev(binary: str) -> Dict:
        """Análisis de reverse engineering."""
        results = {"binary": binary, "findings": [], "tools": []}
        
        # Basic file info
        try:
            cmd = f"file {binary}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=30)
            results["file_info"] = result.stdout.strip()
            results["tools"].append("file")
        except Exception:
            pass
        
        # Strings
        try:
            cmd = f"strings {binary}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            results["strings_sample"] = "\n".join(result.stdout.split("\n")[:20])
            results["tools"].append("strings")
        except Exception:
            pass
        
        # Check if packed
        if "UPX" in results.get("file_info", ""):
            results["findings"].append("Binary appears to be packed with UPX")
            results["suggestions"] = ["Run: upx -d binary"]
        
        results["suggestions"] = [
            "Use Ghidra for decompilation",
            "Use radare2: r2 -A binary",
            "Check with binwalk for embedded files",
        ]
        
        return results
