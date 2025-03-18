"""
Pygame helper scripts
"""

from .g import screen, musicManager#, richPresence
from .keys import keychecks
from .actor import Actor
from .background import bg, drawBackgrounds

__all__ = [
    "Actor",
    "bg",
    "drawBackgrounds",
    "keychecks",
    "screen"
]

__title__ = "Game"
__author__ = "_Ghostboo__"
__copyright__ = "Copyright (c) 2025 _Ghostboo__"
__license__ = "MIT"
__version__ = "5.1.0"