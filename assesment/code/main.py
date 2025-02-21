import pgzero
import pygame
import pgzrun
import random
import time
print('Trying to import typing')
try:
    from typing import Optional
    print('Typing has been imported succesfully')
except ImportError:
    from typing_extensions import Optional
    print('Typing failed, falling back to typing_extensions')

class Actor():
    def __init__(image: str, pos: Optional(tuple(int, int))):
        pass