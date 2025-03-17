"""
Global definitions for the game module
"""
from pygame.display import set_mode as __setMode
from .music import MusicManager as __MusicManager

screen = __setMode((1280, 720))
musicManager = __MusicManager()
