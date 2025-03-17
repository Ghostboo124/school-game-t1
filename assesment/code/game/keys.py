from numpy import sqrt
from pygame import K_LEFT, K_RIGHT, K_d, K_a, K_SPACE, K_q, K_LSHIFT, K_RSHIFT
from sys import exit, stderr

try:
    from typing import Optional, TYPE_CHECKING
except (ImportError, OSError):
    from typing_extensions import Optional

if TYPE_CHECKING:
    from .actor import Actor
else:
    class Actor: None

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

def keychecks(keys, actor: Actor, spd, dt: Optional[float] = None, blockJump: Optional[bool] = False) -> float:
    """
    Game Files
    """
    # Has dt been supplied?
    if dt == None:
        dt = 60/1000

    if keys[K_LEFT] or keys[K_a]:
        kLeft = 1
    else:
        kLeft = 0
    if keys[K_RIGHT] or keys[K_d]:
        kRight = 1
    else:
        kRight = 0
    # if keys[pygame.K_UP] or keys[pygame.K_w]:  ### These are for going up and down, which will be disabled, might just remove these lines
    #     kUp = 1
    # else:
    #     kUp = 0
    # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #     kDown = 1
    # else:
    #     kDown = 0
    if keys[K_SPACE] and not blockJump:
        actor.jump(actor.m, actor.v)
    if keys[K_q] and keys[K_LSHIFT] or keys[K_RSHIFT]:
        raise Exception("Keybind Interrupt")
    if keys[K_q]:
        exit(0)

    moveH = kRight - kLeft
    # moveV = kDown - kUp

    Mag = sqrt((moveH * moveH))#+(moveV * moveV))

    if Mag == 0:
        Mag = 1 * dt
    
    moveX = (moveH/Mag) * spd
    # moveY = (moveV/Mag) * spd

    return moveX