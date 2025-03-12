"""
A Game by Alexander Perkins
© Alexander Perkins 2025

Error Codes:
    To check the error code, you can check the %errorlevel% variable in windows
    0 All is well, nothing has gone wrong
    1 Import Error has occured
    5 Unknown error has occured, please refer to the error message
"""

# Imports
try:
    #import pgzero
    import pygame
    #import pgzrun
    import random
    import math
    import numpy
    import time
    import os
    import sys
    print('Trying to import typing')
    # Need to try typing then typing_extensions for backwards compatability
    try:
        from typing import Optional
        print('Typing has been imported succesfully')
    except ImportError:
        try:
            from typing_extensions import Optional
            print('Typing failed, falling back to typing_extensions')
        except Exception as e:
            print('typing_extensions has failed to import, printing details now:\n\t' + e)
except Exception as e:
    # Can't use my exit function here, and I am not willing to place it earlier for organisational reasons
    print("Unknown error occured, printing details now:\n\t" + e)
    sys.exit(1)

# Initialisation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Code
def exit(errorlevel: int = 5, details: Optional[Exception | str | None] = None) -> int:
    """
    My custom exit function with detail printing
    Args:
        errorlevel: The code to exit with, defaults to 5 (unknown error)
        details: The details of the error code (Optional)
    """
    if errorlevel != 0:
        sys.stderr.write(f"Exiting with error code: {errorlevel}\n")
    if details != None:
        if type(details) != str:
            sys.stderr.write(f"Type: {type(details)}, Details:\n\t{details}")
        else:
            sys.stderr.write(f"Details:\n\t{details}")
    sys.exit(errorlevel)

class Actor(pygame.sprite.Sprite):
    def __init__(self, image: str, name: str, disabled: True | False, pos: Optional[tuple[int, int]] | Optional[numpy.ndarray] = (0,0), zoom: Optional[float] = 1.0, rotation: Optional[float] = 0.0):
        """
        An Actor class so that this code is nicely wrapped up instead of having multiple instances existing in the main function
        Args:
            image: The image to set this Actor to be displayed as, string with the path to the image
            name: The name of the Actor, string
            pos: The position to set the Actor to in the format of (x, y), (Defaults to (0,0))
            zoom: How much to zoom the image in by, Optional, defaults to 1.0
            rotation: How much to rotate the image, Optional, defaults to 0.0
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
            print(pos)
        self.pos = pos
        print(self.pos[0])
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.destroyed = False
    
    def draw(self):
        """
        A Function to draw the actor to the screen, doesn't take any arguments
        """
        # Checking if the image is outside the bounding box (The screen size)
        if self.destroyed == False:
            if self.x < 0:
                #self.x = 0
                self.x = screen.get_width() - self.image.get_width() - 30
            elif self.x > screen.get_width() - self.imageBig.get_width():
                #self.x = screen.get_width() - self.image.get_width() - 40
                self.x = 0

            if self.y < 0:
                #self.y = 0
                self.destroy()
            elif self.y > screen.get_height() - self.imageBig.get_height() - 40:
                #self.y = screen.get_height() - self.image.get_height() - 40
                self.destroy()

            # Updating the position if it gets changed
            self.pos = (self.x, self.y)
            # Putting the image onto the screen
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
        if self.destroyed == False:
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
        self.destroyed = True
        self.image = ""
        self.x, self.y = numpy.array((60054854, 756483))
        self.pos = (self.x, self.y)
        print(self.x, self.y)
    
    def iscolliding(self, object: numpy.ndarray | tuple):
        # print(self.pos)
        if type(object) == numpy.ndarray or type(object) == tuple and len(object) == 2:
            print(f"({object[0], object[1]})")
        elif type(object) != numpy.ndarray:
            print(f"Wierd, the type of the object is {type(object)}")
        elif len(object) != 2:
            print(f"Wierd, the length is wrong: {len(object)}")
        # print(object.pos)
    def jump(self):
        return NotImplementedError("jump function isn't implimented yet")

spd = 2
zoom = 2.0
spNugget = Actor("images\\spNugget.png", "spNugget", zoom=zoom, pos=numpy.array((0,380)), disabled=False)

def main(dt: float, fps: int) -> int:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        kLeft = 1
    else:
        kLeft = 0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        kRight = 1
    else:
        kRight = 0
    # if keys[pygame.K_UP] or keys[pygame.K_w]:
    #     kUp = 1
    # else:
    #     kUp = 0
    # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #     kDown = 1
    # else:
    #     kDown = 0
    if keys[pygame.K_SPACE]:
        spNugget.jump()
    if keys[pygame.K_1]:
        fps = 10
    if keys[pygame.K_2]:
        fps = 20
    if keys[pygame.K_3]:
        fps = 30
    if keys[pygame.K_4]:
        fps = 40
    if keys[pygame.K_5]:
        fps = 50
    if keys[pygame.K_6]:
        fps = 60
    if keys[pygame.K_7]:
        fps = 120
    if keys[pygame.K_8]:
        fps = 240
    if keys[pygame.K_9]:
        fps = 480
    if keys[pygame.K_0]:
        fps = 0

    moveH = kRight - kLeft
    # moveV = kDown - kUp

    Mag = math.sqrt((moveH * moveH))#+(moveV * moveV))

    if Mag == 0:
        Mag = 1 * dt
    
    #print((moveH/Mag) * spd, (moveV/Mag))
    
    moveX = (moveH/Mag) * spd
    # moveY = (moveV/Mag) * spd

    if spNugget.destroyed == False:
        spNugget.update(spNugget.x + moveX, spNugget.y, "images\\spNugget.png", zoom=zoom)
        spNugget.draw()
        # print(spNugget.pos)
    return fps
    

if __name__ == "__main__":
    try:
        tick = 0
        spNugget.iscolliding(numpy.array((0, 0)))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
            screen.fill("black")
            if tick != 0:
                print(f"FPS: {clock.get_fps()} DT: {dt} Raw Time: {clock.get_rawtime()} Time: {clock.get_time()}")
                fps = main(dt, fps)
                dt = clock.tick(fps) / 1000
            else:
                dt = clock.tick(2) / 1000
                fps = 60
                tick += 1
            pygame.display.flip()
    except Exception as e:
        exit(e)
    except KeyboardInterrupt:
        pygame.quit()
        exit("Please don't keyboard interupt, closing safely")
    
pygame.quit()
exit(errorlevel=0)