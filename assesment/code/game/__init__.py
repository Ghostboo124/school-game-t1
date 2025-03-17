"""
The required files for my game
"""

from .g import screen
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