from PIL.ImageFile import ImageFile
import pygame
from pytmx import load_pygame
from numpy import array, dtype, ndarray
from PIL import Image
import os

from pytmx.pytmx import TiledMap

pygame.display.init()
pygame.display.set_mode((1, 1))

try:
    from typing import Optional, Any
except ImportError:
    try:
        print("Error whilst importing typing!\nFalling back to typing_extensions")
        from typing_extensions import Optional, Any
    except ImportError:
        print("Error has occured whilst importing typing_extensions!")
        print("Using internal typing, this may not be up to date, please fix your python.")
        from .__typing import Optional, Any

class map:
    def __init__(self):
        self.previousMap: None | str = None
        self.currentMap: str = "map1"
        self.nextMap: None | str = "map2"
        self.maps: ndarray[tuple[int, ...], dtype[Any]]= array(object=[ # type: ignore
            "map1",
            "map2",
            "map3",
            "map4"
        ], dtype=str)
    
    def getNextMap(self) -> str | None:
        for i in range(len(self.maps)):
            if self.maps[i] == self.currentMap:
                if self.maps[-1] == self.maps[i]:
                    self.nextMap: None | str = None
                    return self.nextMap
                if isinstance(self.maps[i + 1], str):
                    self.nextMap: None | str = self.maps[i + 1]
                    return self.nextMap
    
    def getPrevMap(self) -> str | None:
        for i in range(len(self.maps)):
            if self.maps[i] == self.currentMap:
                if 0 == i:
                    self.previousMap = None
                    return self.previousMap
                self.previousMap = self.maps[i - 1]
                return self.previousMap
    
    def switchMap(self, map: Optional[str] = None) -> str:
        if map == None:
            if isinstance(self.getNextMap, str):
                self.currentMap = self.getNextMap()
            else:
                return self.currentMap
        else:
            if map not in self.maps:
                return map
            else:
                self.currentMap = map
        return self.currentMap

def loadGifFrames(path: str) -> list[pygame.Surface]:
    if not isinstance(path, str):
        raise ValueError(f"Path ({path}) should be a string representing the file path, not {type(path)}")
    
    image: ImageFile = Image.open(fp=path)
    frames: list[pygame.Surface] = []
    try:
        while True:
            frame: Image.Image = image.copy()
            frame = frame.convert(mode="RGBA")
            frames.append(pygame.image.fromstring(bytes=frame.tobytes(), size=frame.size, format=frame.mode)) # type: ignore
            image.seek(frame=image.tell() + 1)
    except EOFError:
        pass
    return frames

class mapElement(pygame.sprite.Sprite):
    def __init__(self, pos: ndarray[float, float] | tuple[float, float], image: str, disabled: bool = True): # type: ignore
        super().__init__()
        if isinstance(pos, tuple):
            self.pos = array(pos)
        else:
            self.pos = pos
        self.imagePath: str = image
        if not image.split(".")[1] == "gif":
            self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
        self.disabled: bool = disabled

    def getRect(self) -> pygame.Rect:
        return self.image.get_rect()

map1: TiledMap = load_pygame(filename=os.path.join("images", "maps", "map1.tmx"))
print(map1)

map2: TiledMap = load_pygame(filename=os.path.join("images", "maps", "map2.tmx"))
print(map2)

map3 = None

map4 = None

pygame.display.quit()