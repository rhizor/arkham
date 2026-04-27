"""
Platform integrations for CTF platforms.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)


class Platform(ABC):
    """Base class for CTF platforms."""
    
    @abstractmethod
    def get_machine_info(self, machine_id: str) -> Dict:
        """Obtiene información de una máquina/room."""
        pass
    
    @abstractmethod
    def submit_flag(self, flag: str) -> bool:
        """Envía una flag al sistema."""
        pass


@dataclass
class HackTheBox(Platform):
    """HackTheBox integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("HTB_API_KEY")
        self.base_url = "https://www.hackthebox.com/api/v4"
    
    def get_machine_info(self, machine_id: str) -> Dict:
        """Obtiene info de una máquina HTB."""
        if not self.api_key:
            return {"error": "HTB_API_KEY not configured"}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.get(
                f"{self.base_url}/machine/{machine_id}", 
                headers=headers, 
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTB API error: {e}")
            return {"error": str(e)}
    
    def submit_flag(self, flag: str) -> bool:
        """Envía una flag a HackTheBox."""
        if not self.api_key:
            logger.warning("HTB_API_KEY not configured - flag not submitted")
            return False
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(
                f"{self.base_url}/machine/flag", 
                headers=headers, 
                json={"flag": flag}, 
                timeout=10
            )
            return resp.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to submit flag: {e}")
            return False


@dataclass
class TryHackMe(Platform):
    """TryHackMe integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("THM_API_KEY")
        self.base_url = "https://tryhackme.com/api"
    
    def get_machine_info(self, room_id: str) -> Dict:
        """Obtiene info de un room THM."""
        if not self.api_key:
            return {"error": "THM_API_KEY not configured"}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.get(
                f"{self.base_url}/room/{room_id}", 
                headers=headers, 
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"THM API error: {e}")
            return {"error": str(e)}
    
    def submit_flag(self, flag: str) -> bool:
        """Envía una flag a TryHackMe."""
        logger.warning("THM flag submission not implemented")
        return False
