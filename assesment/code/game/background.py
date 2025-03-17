"""
The file to deal with backgrounds
"""
import pygame
from os.path import join as joinPath
from .g import screen

try:
    from typing import Optional
except:
    try:
        print("Error whilst importing typing!\nFalling back to typing_extensions")
        from typing_extensions import Optional
    except:
        print("Error has occured whilst importing typing_extensions!")
        print("Using internal typing, this may not be up to date, please fix your python.")
        from ._typing import Optional
class bg:
    def __init__(self, image: str, xchange: Optional[int] = None):
        """
        A Background class
        Args:
            image: The image for the background, str
            xchange: How much to change the x by every frame, int (Optional)
        """
        self.x = 0
        self.xChange = xchange
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.imageFiller = self.image.copy()
        self.imageFillerX = self.x + self.image.get_width()

    def loadBackground(self, newImage: str) -> None:
        self.image = pygame.image.load(newImage)
        self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.imageFiller = self.image.copy()
        self.imageFillerX = self.x + self.image.get_width()


    def drawBackground(self) -> None:
        if self.xChange is not None:
            self.x -= self.xChange
            self.imageFillerX -= self.xChange

            if self.x <= -self.image.get_width():
                self.x = self.image.get_width()
            if self.imageFillerX <= -self.image.get_width():
                self.imageFillerX = self.image.get_width()
        
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.imageFiller, (self.imageFillerX, 0))

def drawBackgrounds(backgrounds: list[bg]):
    for i in backgrounds:
        i.drawBackground()

backgrounds = [
    bg(joinPath("images", "bg1.png"), 1),
    bg(joinPath("images", "bg2.png"), 2),
    bg(joinPath("images", "bg3.png"), 2.5)
]