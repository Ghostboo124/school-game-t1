"""
The Actor file
"""

from PIL.ImageFile import ImageFile
from numpy._typing._array_like import NDArray
import pygame, numpy
from PIL import Image
from sys import stderr
from sys import exit as __exit
from .g import screen, map
from .keys import keychecks
from .background import drawBackgrounds, backgrounds

try:
    from typing import Optional, TYPE_CHECKING
except (ImportError, OSError):
    try:
        print("Error whilst importing typing!\nFalling back to typing_extensions")
        from typing_extensions import Optional, TYPE_CHECKING
    except ImportError:
        print("Error has occured whilst importing typing_extensions!")
        print("Using internal typing, this may not be up to date, please fix your python.")
        from .__typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .actor import Actor
else:
    class Actor: pass

def loadGifFrames(path: str) -> list[pygame.Surface]:
    if not isinstance(path, str):
        raise ValueError(f"Path ({path}) should be a string representing the file path, not {type(path)}")
    
    image: ImageFile = Image.open(fp=path)
    frames: list[pygame.Surface] = []
    try:
        while True:
            frame: Image.Image = image.copy()
            frame = frame.convert(mode="RGBA")
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)) # type: ignore < for pylance
            image.seek(frame=image.tell() + 1)
    except EOFError:
        pass
    return frames

def raycast(start: numpy.ndarray, end: numpy.ndarray, obstacles: list) -> bool:
    """
    Perform raycasting to check for line of sight between start and end positions.

    Args:
        start (numpy.ndarray): The starting position of the ray.
        end (numpy.ndarray): The ending position of the ray.
        obstacles (list): A list of obstacle rects.

    Returns:
        bool: True if there is a clear line of sight, False otherwise.
    """#TODO: UPDATE PROPERLY
    if obstacles == None:
        return True
    direction = end - start
    distance= numpy.linalg.norm(x=direction)
    direction = direction / distance  # Normalize the direction vector

    steps = int(distance)
    for i in range(steps):
        point = start + direction * i
        for obstacle in obstacles:
            if obstacle.collidepoint(point):
                return False
    return True

def exit(errorlevel: int = -1, details: Optional[Exception | str] = None) -> int:
    """
    My custom exit function with detail printing
    Args:
        errorlevel: The code to exit with, defaults to -1 (unknown error)
        details: The details of the error code (Optional)
    """
    if errorlevel != 0:
        stderr.write(f"Exiting with error code: {errorlevel}\n")
    if details is not None:
        if not isinstance(details, str):
            stderr.write(f"Type: {type(details)}, Details:\n\t{details}")
        else:
            stderr.write(f"Details:\n\t{details}")
    __exit(errorlevel)

class Animation:
    def __init__(self, frames, frame_duration) -> None:
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_accumulator = 0

    def update(self, dt) -> None:
        self.time_accumulator += dt
        if self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]

class Actor(pygame.sprite.Sprite):
    def __init__(self: Actor, image: str, name: str, disabled: bool, pos: Optional[numpy.ndarray[float, float]] = numpy.array(object=(0, 0), dtype=float), animation_path: Optional[str] = None, zoom: float = 1.0, rotation: float = 0.0, m: int = 1, v: int = 5, spd: int = 1): # type: ignore
        """
        An Actor class so that this code is nicely wrapped up instead of having multiple instances
        Args:
            image: The image to set this Actor to be displayed as, string with the path to the image
            name: The name of the Actor, string
            disabled: Is the Actor disabled, boolean
            pos: The position to set the Actor to in the format of (x, y), (Defaults to (0,0)), either a tuple of a numpy array
            zoom: How much to zoom the image in by, Optional, defaults to 1.0, float
            rotation: How much to rotate the image, Optional, defaults to 0.0, float
            m: Mass, defaults to 1, int
            v: Velocity, defaults to 5, int
            spd: The speed of the Actor, defaults to 1, int
        """# TODO: UPDATE THIS!
        super().__init__()
        try:
            if image.split(sep=".")[1] == "gif":
                self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
                self.image.set_colorkey(pygame.Color((0, 0, 0)))
            else:
                # print(image.split("."))
                self.image = pygame.image.load(image).convert_alpha()
        except Exception as e:
            exit(errorlevel=2, details=e)
        self.imageBig: pygame.Surface = pygame.transform.rotozoom(self.image, rotation, zoom)
        self.name: str = name  
        self.pos: numpy.ndarray[float, float] = pos # type: ignore
        self.x: float = self.pos[0]
        self.y: float = self.pos[1]
        self.disabled: bool = disabled
        self.m: int = m
        self.staticM: int = self.m
        self.v: int = v
        self.staticV: int = self.v
        self.spd: int = spd
        self.isJumping: bool = False
        self.jumpVelocity: int = 0
        self.gravity: int = 1
        self.animation: Animation
        # print(f"Image: {image} name: {name} disabled: {disabled} pos: {pos} animation_path: {animation_path} zoom: {zoom} rotation: {rotation} m: {m} v: {v} spd: {spd}")
        if None != animation_path:
            frames: list[Surface] = loadGifFrames(path=animation_path) # type: ignore
            self.animation = Animation(frames=frames, frame_duration=100)
    
    def draw(self: Actor) -> None:
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
            elif self.y > screen.get_height() - self.imageBig.get_height() - 40: ### These haven't been replaced by the character getting destroyed
                #self.y = screen.get_height() - self.image.get_height() - 40
                self.destroy()

            # Updating the position if it gets changed and putting the image onto the screen
            self.pos = numpy.array(object=(self.x, self.y), dtype=float) # type: ignore
            screen.blit(source=self.imageBig, dest=tuple(self.pos))
    
    def update(self: Actor, x: float, y: float, image: Optional[str] = None, zoom: float = 1.0, rotation: float = 0.0, dt: float = 60/1000):
        """
        A Function to update the Actor
        Args:
            x: The x position
            y: The y position
            image: The image path, Optional, defaults to None
            zoom: The zoom value as a float, defaults to 1.0
            rotation: The rotation, defaults to 0.0
        """#TODO: UPDATE THIS DOCSTRING
        if self.disabled == False:
            #print(f"Updating Actor: {self.name}")
            if self.animation != None:
                self.animation.update(dt=dt)
            if image is not None:
                self.image = pygame.image.load(image).convert_alpha()
                self.imageBig = pygame.transform.rotozoom(self.image, rotation, zoom)
            self.pos = numpy.array(object=(x, y), dtype=float) # type: ignore
            self.x = self.pos[0]
            self.y = self.pos[1]

    def moveTowards(self: Actor, target: Actor | numpy.ndarray[float, float], dt: float) -> None: # type: ignore
        if isinstance(target, Actor):
            targetPos: numpy.ndarray= target.pos
        elif isinstance(target, numpy.ndarray) or isinstance(target, dict):
            targetPos: numpy.ndarray = target
        # print(raycast(self.pos, targetPos, None))

        x: float = targetPos[0] - self.x
        y: float = targetPos[1] - self.y
        direction: numpy.ndarray = numpy.array(object=(x, y))
        distance: numpy.floating = numpy.linalg.norm(direction)
        
        if distance > 0:
            direction = direction / distance # Normalise the vector
            if direction[1] <= -1 or direction[1] >= 0:
                # print(direction[1])
                return
            self.pos += direction * self.spd * dt # type: ignore
            self.x, self.y = self.pos
            # print(f"New Pos: {self.pos}")
        else:
            if isinstance(target, Actor):
                self.attack(target=target)
            else:
                print("Can't attack, target is not an Actor")
    
    def attack(self: Actor, target: Actor):
        print("No!")

    def destroy(self: Actor) -> None:
        self.disabled = True
        self.x, self.y = numpy.array(object=(60054854, 756483))
        self.pos = numpy.array(object=(self.x, self.y)) # type: ignore
        self.image = "" # type: ignore 
    def iscolliding(self, object: numpy.ndarray | tuple | Actor) -> None:
        # print(self.pos)
        if isinstance(object, (numpy.ndarray, tuple)) and len(object) == 2:
            # print(f"({object[0], object[1]})")
            pass
        elif not isinstance(object, numpy.ndarray):
            # print(f"Weird, the type of the object is {type(object)}")
            pass
        elif len(object) != 2:
            # print(f"Weird, the length is wrong: {len(object)}")
            pass
        raise NotImplementedError("This isn't implimented yet")
    
    def jump(self) -> None:
        """
        A Function to make an actor jump
        Args:
            v: the objects initial jump velocity
        """
        if self.isJumping == False:
            self.isJumping = True
            self.jumpVelocity = self.v

    def applyGravity(self, moveX: float, dt: float) -> None:
        if self.isJumping == True:
            self.y -= self.jumpVelocity
            self.jumpVelocity -= self.gravity
            if self.y >= 380:
                self.y = 380
                self.isJumping = False
            self.x += moveX
        if self.y < 380 and self.isJumping == False:
            self.y -= self.jumpVelocity
            self.jumpVelocity -= self.gravity

class uiElement(Actor):
    def __init__(self, image, name, disabled, pos = (0, 0), zoom = 1, rotation = 0):
        super().__init__(image=image, name=name, disabled=disabled, pos=pos, animation_path=None, zoom=zoom, rotation=rotation)
        # print(self.image)

    def draw(self) -> None:
        """
        Draws the UI Element to the screen unless disabled
        """
        if self.disabled == False:
            screen.blit(source=self.imageBig, dest=tuple(self.pos))