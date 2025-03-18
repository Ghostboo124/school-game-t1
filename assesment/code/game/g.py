"""
Global definitions for the game module
"""
from pygame.display import set_mode as __setMode
from pypresence import Presence as __Presence
from .music import MusicManager as __MusicManager

screen = __setMode((1280, 720))
musicManager = __MusicManager()
# richPresence = __Presence()
