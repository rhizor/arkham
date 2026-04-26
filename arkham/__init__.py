"""
ARKHAM - Package initialization.
"""

__version__ = "1.0.0"
__author__ = "rhizor"
__license__ = "MIT"

from .models import Challenge, Command
from .tools import CTFTools
from .platforms import Platform, HackTheBox, TryHackMe
from .solvers import ChallengeSolver
from .agent import CTFAgent

__all__ = [
    "Challenge",
    "Command",
    "CTFTools",
    "Platform",
    "HackTheBox",
    "TryHackMe",
    "ChallengeSolver",
    "CTFAgent",
    "__version__",
]
