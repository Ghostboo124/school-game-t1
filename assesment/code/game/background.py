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
        self.xChange = xchange
        self.image = self.__loadAndScale(image)
        self.imageWidth = self.image.get_width()
        self.imageFillerX = self.x + self.imageWidth
    
    def __loadAndScale(self, image_path: str) -> pygame.Surface:
        """
        A private function to load and scale an image
        Args:
            image_path: The path to the image, str
        """
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, (screen.get_width(), screen.get_height()))

    def loadBackground(self, newImage: str) -> None:
        """
        A Function to change the background image
        Args:
            newImage: The path to the new image, str
        """
        self.image = self.__loadAndScale(newImage)
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
                self.x = self.imageWidth
            if self.imageFillerX <= -self.imageWidth:
                self.imageFillerX = self.imageWidth + self.x
        
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.imageFillerX, 0))

def drawBackgrounds(backgrounds: list[bg]):
    for i in backgrounds:
        i.drawBackground()

backgrounds = [
    bg(joinPath("images", "bg1.png"), 1),
    bg(joinPath("images", "bg2.png"), 2),
    bg(joinPath("images", "bg3.png"), 2.5)
]