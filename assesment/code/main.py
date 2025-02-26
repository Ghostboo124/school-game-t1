import pgzero
import pygame
import pgzrun
import random
import math
import time
import os
print('Trying to import typing')
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
    print("Unknown error occured, printing details now:\n\t" + e)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

class Actor():
    def __init__(self, image: str, name: str, pos: Optional[tuple[int, int]] = (0,0)):
        self.image = pygame.image.load(image).convert()
        self.name = name
        self.pos = pos
        #print(type(self.pos))
        self.x = self.pos[0]
        self.y = self.pos[1]
    
    def draw(self):
        #print(f"Drawing Actor: {self.name}")
        screen.blit(self.image, self.pos)
    
    def update(self, x: int, y: int, image = Optional[str]):
        """
        A Function to update the Actor
        Args:
            x: The x position
            y: The y position
        """
        #print(f"Updating Actor: {self.name}")
        if type(image) != str:
            pass
        else:
            self.image = pygame.image.load(image).convert()
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        print(self.pos)

test = Actor("images\\spNugget.png", "spNugget")
spd = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    screen.fill("black")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        kLeft = 1
    else:
        kLeft = 0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        kRight = 1
    else:
        kRight = 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        kUp = 1
    else:
        kUp = 0
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        kDown = 1
    else:
        kDown = 0

    moveH = kRight - kLeft
    moveV = kDown - kUp

    Mag = math.sqrt((moveH * moveH)+(moveV * moveV))

    if Mag == 0:
        Mag = 1
    
    print((moveH/Mag) * spd, (moveV/Mag))
    
    moveX = (moveH/Mag) * spd
    moveY = (moveV/Mag) * spd

    test.update(test.x + moveX, test.y + moveY, "images\\spNugget.png")
    test.draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000