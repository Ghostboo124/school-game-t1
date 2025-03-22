"""
A Game by Alexander Perkins
© Alexander Perkins 2025

Error Codes:
    To check the error code, you can check the %errorlevel% variable in windows
    -1 Unknown error has occured, please refer to the error message
    0  All is well, nothing has gonew wrong
    1  Import Error has occured
"""

# Imports
from game.actor import Actor, uiElement


try:
    import pygame
    import random
    import numpy
    import time
    import os
    import sys
    from game import Actor, uiElement, bg, map
    from game import keychecks, drawBackgrounds, drawMap
    from game import screen, musicManager, map1, map2, map3, map4
    from game.background import backgrounds
    print('Trying to import typing')
    # Need to try typing then typing_extensions for backwards compatibility
    try:
        from typing import Optional
        print('Typing has been imported successfully')
    except ImportError:
        try:
            from typing_extensions import Optional
            sys.stderr.write('Typing failed, falling back to typing_extensions')
        except (ImportError, OSError):
            sys.stderr.write("Importing custom typing, this doesn't get updated, please fix your python")
            from game.__typing import Optional
        except Exception as e:
            sys.stderr.write(f'typing_extensions has failed to import, printing details now:\n\t{e}')
except ImportError as e:
    print(f"Something has gone wrong while importing something, printing details now:\n\t{e.msg}")
except Exception as e:
    # Can't use my exit function here, and I am not willing to place it earlier for organisational reasons
    print(f"Unknown error occured, printing details now:\n\t{e}")
    sys.exit(1)

# Initialisation
pygame.init()
# Screen has been defined in the `game` module
# musicManager has been defined in the `game` module
# richPresence has been defined in the `game` module
# map has been defined in the `game` module
backgroundsPause = list[bg]()
tint = list[bg]()
for i in backgrounds:
    backgroundsPause.append(bg(i.imagePath))
    backgroundsPause[-1].x = i.x
    backgroundsPause[-1].imageFillerX = i.imageFillerX
tint.append(bg(os.path.join("images", "darkFilter.png")))
clock = pygame.time.Clock()
running = True
paused = False
dt = 0
debug = 0

# Custom Exit Function
def exit(errorlevel: int = -1, details: Optional[Exception | str | None] = None) -> int:
    """
    My custom exit function with detail printing
    Args:
        errorlevel: The code to exit with, defaults to -1 (unknown error)
        details: The details of the error code (Optional)
    """
    if errorlevel != 0:
        sys.stderr.write(f"Exiting with error code: {errorlevel}\n")
    if details is not None:
        if not isinstance(details, str):
            sys.stderr.write(f"Type: {type(details)}, Details:\n\t{details}")
        else:
            sys.stderr.write(f"Details:\n\t{details}")
    sys.exit(errorlevel)

spd = 2
rot = 0
zoom = 2.0
v = 10
m = 1
spNugget = Actor(image=os.path.join("images", "spNugget.png"), name="spNugget", disabled=False, pos=numpy.array(object=(0, 200), dtype=float), animation_path=os.path.join("images", "spNuggetIdle.gif"), zoom=zoom, rotation=rot, m=m, v=v, spd=spd) # type: ignore
spSkele  = Actor(image=os.path.join("images", "spSkeleIdle.gif"), name="spSkele", disabled=False, pos=numpy.array(object=(380, 380), dtype=float), animation_path=os.path.join("images", "spSkeleIdle.gif"), zoom=4, rotation=0, m=1, v=5, spd=20) # type: ignore

spClose = uiElement(image=os.path.join("images", "closeUp.png"), name="spClose", disabled=True, pos=(50, 50), zoom=4, rotation=0)
spPlay  = uiElement(image=os.path.join("images", "playUp.png"),  name="spPlay",  disabled=True, pos=(114, 50), zoom=4, rotation=0)

def main(dt: float, fps: int) -> int:
    keys = pygame.key.get_pressed()
    moveX: float = keychecks(keys, spNugget, spd, dt, False)
    drawBackgrounds(backgrounds)
    drawMap(map1)
    for background in backgrounds:
        for pauseBackground in backgroundsPause:
            if background.imagePath != pauseBackground.imagePath:
                continue
            pauseBackground.x = background.x
            pauseBackground.imageFillerX = background.imageFillerX

    # spNugget.destroy()
    if spNugget.disabled == False:
        spNugget.applyGravity(moveX=moveX/2, dt=dt)
        spNugget.update(x=spNugget.x + moveX, y=spNugget.y, image="images\\spNugget.png", zoom=zoom, dt=dt)
        spNugget.draw()
        if debug:
            print(spNugget.pos)
    
    if spSkele.disabled == False:
        if random.randint(0, 100) in range(0,90):
            spSkele.moveTowards(target=spNugget, dt=dt)
        else:
            print("We caught an else!")
        spSkele.applyGravity(moveX=0, dt=dt)
        spSkele.update(x=spSkele.x, y=spSkele.y, dt=dt)
        spSkele.draw()
    return fps

if __name__ == "__main__":
    try:
        tick = 0
        # spNugget.iscolliding(numpy.array((0, 0)))
        if "/nomusic" not in sys.argv:
            musicManager.loadAndPlay(music_file=os.path.join("music", "chill4.ogg"), namehint="Chill No.4", loops=-1)
        #richPresence.connect()
        # musicManager.loadAndPlay(os.path.join("music", "credence.ogg"), "Credence (For  the Uninitiated)", -1)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE: 
                        paused = not paused
                        if paused == True:
                            musicManager.pause()
                        else:
                            musicManager.play()
            screen.fill("black")
            # print(paused)
            if paused == False:
                if tick != 0:
                    # print(f"FPS: {clock.get_fps()} DT: {dt} Raw Time: {clock.get_rawtime()} Time: {clock.get_time()}")
                    fps: int = main(dt=dt, fps=fps)
                    dt: float = clock.tick(fps) / 1000
                else:
                    dt = clock.tick(2) / 1000
                    fps = 60
                    tick += 1
                pygame.display.flip()
                # richPresence.update(pid=os.getpid(), activity_type=0, details="Alex's Assigment")
            else:
                # Things that were there before + tint
                drawBackgrounds(backgroundsPause)
                spNugget.draw()
                spSkele.draw()
                drawBackgrounds(tint)

                # Pause menu UI and extra scripts
                keychecks(pygame.key.get_pressed(), spNugget, spd, dt, True)
                spClose.disabled = False
                spPlay.disabled = False
                spClose.draw()
                spPlay.draw()

                pygame.display.flip()
    # except Exception as e:
    #     exit(errorlevel=-1, details=e)
    except KeyboardInterrupt:
        pygame.quit()
        exit(details="Please don't keyboard interrupt, closing safely")

    pygame.quit()
    exit(errorlevel=0)