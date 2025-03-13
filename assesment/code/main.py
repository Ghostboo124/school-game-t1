"""
A Game by Alexander Perkins
© Alexander Perkins 2025

Error Codes:
    To check the error code, you can check the %errorlevel% variable in windows
    -1 Unknown error has occured, please refer to the error message
    0  All is well, nothing has gone wrong
    1  Import Error has occured
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
    from game import screen, Actor, keychecks
    #from game import screen, pygame, math, numpy
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
# Screen has been defined in the `game` module
clock = pygame.time.Clock()
running = True
dt = 0
debug = 0

# Code
def exit(errorlevel: int = -1, details: Optional[Exception | str | None] = None) -> int:
    """
    My custom exit function with detail printing
    Args:
        errorlevel: The code to exit with, defaults to -1 (unknown error)
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

spd = 2
rot = 0
zoom = 2.0
v = 5
m = 1
spNugget = Actor(os.path.join("images", "spNugget.png"), "spNugget", False, numpy.array((0, 380)), zoom, rot, m, v, spd)
def main(dt: float, fps: int) -> int:
    keys = pygame.key.get_pressed()
    moveX = keychecks(keys, spNugget, spd, dt, False)

    if spNugget.disabled == False:
        spNugget.update(spNugget.x + moveX, spNugget.y, "images\\spNugget.png", zoom=zoom)
        spNugget.draw()
        if debug:
            print(spNugget.pos)
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
                # print(f"FPS: {clock.get_fps()} DT: {dt} Raw Time: {clock.get_rawtime()} Time: {clock.get_time()}")
                fps = main(dt, fps)
                dt = clock.tick(fps) / 1000
            else:
                dt = clock.tick(2) / 1000
                fps = 60
                tick += 1
            pygame.display.flip()
    except Exception as e:
        exit(-1, e)
    except KeyboardInterrupt:
        pygame.quit()
        exit("Please don't keyboard interupt, closing safely")
    
pygame.quit()
exit(errorlevel=0)