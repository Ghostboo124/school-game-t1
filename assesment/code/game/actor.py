"""
The Actor file
"""
from .g import screen
import pygame, numpy
from sys import exit, stderr
from .keys import keychecks

try:
    from typing import Optional
except (ImportError, OSError):
    from typing_extensions import Optional

def exit(errorlevel: int = -1, details: Optional[Exception | str] = None) -> int:
    """
    My custom exit function with detail printing
    Args:
        errorlevel: The code to exit with, defaults to -1 (unknown error)
        details: The details of the error code (Optional)
    """
    if errorlevel != 0:
        stderr.write(f"Exiting with error code: {errorlevel}\n")
    if details != None:
        if type(details) != str:
            stderr.write(f"Type: {type(details)}, Details:\n\t{details}")
        else:
            stderr.write(f"Details:\n\t{details}")
    exit(errorlevel)

class Actor(pygame.sprite.Sprite):
    def __init__(self, image: str, name: str, disabled: bool, pos: Optional[tuple[int, int]] | Optional[numpy.ndarray] = (0,0), zoom: Optional[float] = 1.0, rotation: Optional[float] = 0.0, m: int = 1, v: int = 5, spd: int = 1):
        """
        An Actor class so that this code is nicely wrapped up instead of having multiple instances existing in the main function
        Args:
            image: The image to set this Actor to be displayed as, string with the path to the image
            disabled: Is the Actor disabled, can be changed internally
            name: The name of the Actor, string
            pos: The position to set the Actor to in the format of (x, y), (Defaults to (0,0))
            zoom: How much to zoom the image in by, Optional, defaults to 1.0
            rotation: How much to rotate the image, Optional, defaults to 0.0
            m: Mass, int
            v: Velocity, int
        """
        super().__init__()
        try:
            self.image = pygame.image.load(image).convert()
        except Exception as e:
            exit(e, 2)
        self.imageBig = pygame.transform.rotozoom(self.image, rotation, zoom)
        self.name = name
        if type(pos) != numpy.ndarray:
            pos = numpy.array(pos)
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.disabled = disabled
        self.m = m
        self.v = v
        self.spd = spd
    
    def draw(self):
        """
        A Function to draw the actor to the screen, doesn't take any arguments
        """
        # Checking if the image is outside the bounding box (The screen size)
        if self.disabled == False:
            if self.x < 0:
                #self.x = 0
                self.x = screen.get_width() - self.image.get_width() - 30
            elif self.x > screen.get_width() - self.imageBig.get_width():
                #self.x = screen.get_width() - self.image.get_width() - 40 ### Commented lines are the original lines that make sure that the 
                self.x = 0                                                 ### character doesn't go off the screen, this has been replaced by
                                                                           ### the character moving to the other side of the screen
            if self.y < 0:
                #self.y = 0
                self.destroy()
            elif self.y > screen.get_height() - self.imageBig.get_height() - 40: ### These haven't been changed over
                #self.y = screen.get_height() - self.image.get_height() - 40
                self.destroy()

            # Updating the position if it gets changed and putting the image onto the screen
            self.pos = (self.x, self.y)
            screen.blit(self.imageBig, self.pos)
    
    def update(self, x: int, y: int, image = Optional[str], zoom: float = 1.0, rotation: float = 0.0):
        """
        A Function to update the Actor
        Args:
            x: The x position
            y: The y position
            zoom: The zoom value as a float, defaults to 1.0
            rotation: The rotation, defaults to 0.0
        """
        if self.disabled == False:
            #print(f"Updating Actor: {self.name}")
            if type(image) != str:
                pass
            else:
                self.image = pygame.image.load(image).convert()
                self.imageBig = pygame.transform.rotozoom(self.image, rotation, zoom)
            self.pos = numpy.array((x, y))
            self.x = self.pos[0]
            self.y = self.pos[1]
            
    def destroy(self):
        self.disabled = True
        self.image = ""
        self.x, self.y = numpy.array((60054854, 756483))
        self.pos = (self.x, self.y)
    
    def iscolliding(self, object: numpy.ndarray | tuple):
        # print(self.pos)
        if type(object) == numpy.ndarray or type(object) == tuple and len(object) == 2:
            print(f"({object[0], object[1]})")
        elif type(object) != numpy.ndarray:
            print(f"Wierd, the type of the object is {type(object)}")
        elif len(object) != 2:
            print(f"Wierd, the length is wrong: {len(object)}")
    def jump(self, m: int, v: int):
        """
        A Function to make an actor jump
        Args:
            m: The objects mass
            v: the objects velocity
        """
        isJump = True
        if self.y == 380:
            while isJump:
                screen.fill(pygame.Color(0, 0, 0))
                F = (1 / 2) * m * (v ** 2)
                self.y -= F
                v -= 1
                if v < 0:
                    m = -1
                if v == -6:
                    v = 5
                    m = 1
                    isJump = False
                keys = pygame.key.get_pressed()
                moveX = keychecks(keys, self, m, v, self.spd, self.dt, True)
                self.update(self.x + moveX, self.y, zoom=2)
                self.draw()
                pygame.display.flip()
                pygame.time.delay(40)