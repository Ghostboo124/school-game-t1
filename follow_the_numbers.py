ignore = True
from random import randint
if ignore == False:
    from pgzero.actor import Actor
    from pgzero.screen import Screen
import pygame

font     = pygame.font.SysFont(None, 24)
pygame.font.init()
WIDTH    = 400
HEIGHT   = 400

dots     = []
lines    = []

next_dot = 0

if ignore == False:
    screen   = Screen()

for dot in range(0, 10):
    actor = Actor("dot", (randint(20, WIDTH-20), randint(20, HEIGHT-20)))
    dots.append(actor)

def draw():
    global font
    font.set_italic(True)

    screen.fill("black")
    number = 1
    for dot in dots:
        dot.draw
        text = font.render(str(number), True, pygame.Color(255, 255, 255))
        screen.blit(text, (dot.x, dot.y + 12))
        number += 1
    for line in lines:
        screen.draw.line(line[0], line[1], (100, 0, 0))