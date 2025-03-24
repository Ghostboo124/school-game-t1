"""
Global definitions for the game module
"""
from pygame import Surface
from pygame.display import set_mode as __setMode__
from pypresence import Presence as __Presence__

from game.pathfinding import Spot
from .music import MusicManager as __MusicManager__
from .map import map as __map__
from .map import map1 as __initialGrid__
from .pathfinding import createGrid as __createGrid__

screen: Surface = __setMode__((1280, 720))
musicManager = __MusicManager__()
gameMap = __map__()
grid: list[list[Spot]] = __createGrid__(mapData=__initialGrid__)
# richPresence = __Presence()
