"""
The file to deal with backgrounds
"""
import pygame
from os.path import join as joinPath
from numpy import ndarray
from pytmx import TiledMap, TiledTileLayer
import pytmx
from .g import screen

try:
    from typing import Optional
except ImportError:
    try:
        print("Error whilst importing typing!\nFalling back to typing_extensions")
        from typing_extensions import Optional
    except ImportError:
        print("Error has occured whilst importing typing_extensions!")
        print("Using internal typing, this may not be up to date, please fix your python.")
        from .__typing import Optional

class bg:
    def __init__(self, image: str, xchange: Optional[int] = None):
        """
        A Background class
        Args:
            image: The path to the image for the background, str
            xchange: How much to change the x by every frame, int (Optional) defaults to None
        """
        self.x = 0
        self.xChange: int | None = xchange
        self.image: pygame.Surface = self.__loadAndScale(image_path=image)
        self.imagePath: str = image
        self.imageWidth: int = self.image.get_width()
        self.imageFillerX: int = self.x + self.imageWidth
    
    def __loadAndScale(self, image_path: str) -> pygame.Surface:
        """
        A private function to load and scale an image
        Args:
            image_path: The path to the image, str
        """
        image: pygame.Surface = pygame.image.load(image_path)
        return pygame.transform.scale(image, (screen.get_width(), screen.get_height()))

    def loadBackground(self, newImage: str) -> None:
        """
        A Function to change the background image
        Args:
            newImage: The path to the new image, str
        """
        self.image = self.__loadAndScale(image_path=newImage)
        self.imageWidth = self.image.get_width()
        self.imageFillerX = self.x + self.imageWidth


    def drawBackground(self) -> None:
        """
        A Function to draw the background image
        """
        if self.xChange is not None:
            self.x -= self.xChange
            self.imageFillerX -= self.xChange

            if self.x <= -self.imageWidth:
                self.x: int = self.imageWidth
            if self.imageFillerX <= -self.imageWidth:
                self.imageFillerX = self.imageWidth + self.x
        
        screen.blit(source=self.image, dest=(self.x, 0))
        screen.blit(source=self.image, dest=(self.imageFillerX, 0))

def drawBackgrounds(backgrounds: list[bg]):
    for i in backgrounds:
        i.drawBackground()

def drawMap(map: TiledMap):
    for layer in map.layers:
        # print(layer)
        # print(map.objects) # type: ignore
        # print(map.layers)
        # for x, y, gid in map.layers[layer].iter_data():
        for x, y, gid in layer.iter_data():
            try:
                screen.blit(map.get_tile_image_by_gid(gid), (x*32, y*32)) # type: ignore
            except Exception as e:
                continue

backgrounds: list[bg] = [
    bg(image=joinPath("images", "bg1.png"), xchange=1),
    bg(image=joinPath("images", "bg2.png"), xchange=2),
    bg(image=joinPath("images", "bg3.png"), xchange=4)
]