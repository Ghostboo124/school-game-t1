"""
Pygame helper scripts
"""

from .g import screen, musicManager, gameMap#, richPresence
from .keys import keychecks
from .actor import Actor, uiElement
from .background import bg, drawBackgrounds, drawMap
from .map import map1, map2, map3, map4, mapElement

__all__: list[str] = [
    "Actor",
    "bg",
    "drawBackgrounds",
    "drawMap",
    "keychecks",
    "screen"
]

__title__ = "Game"
__author__ = "_Ghostboo__"
__copyright__ = "Copyright (c) 2025 _Ghostboo__"
__license__ = "MIT"
__version__ = "5.1.0"