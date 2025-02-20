"""
A Game where you play as a fox and collect coins
"""
import pygame
import time
from random import randint
import coin_collector as variables
import math

font = pygame.font.SysFont(None, 24)
WIDTH = 400
HEIGHT = 400
score = 0
highScore = 0
gameOver = False

fox = Actor("fox")
fox.x, fox.y = (100, 100)

coin = Actor("coin")
coin.x, coin.y = (200, 200)

def draw() -> None:
    """
    The draw function
    """
    global font
    global score
    global highScore
    global gameOver

    screen.fill("green")
    fox.draw()
    coin.draw()
    #t0 = time.time()
    counter1 = font.render(f"Score: {score}", True, pygame.Color(255,255,255))
    #print("Time needed for Font creation: ", time.time() - t0)
    screen.blit(counter1, (10, 10))
    if gameOver:
        screen.clear()
        screen.fill("red")
        gameOverText = font.render(f"Game Over, final score: {score}", True, pygame.Color(255,255,255))
        screen.blit(gameOverText, (2, HEIGHT/2))
        

def place_object(actor) -> None:
    if actor == coin:
        coin.x, coin.y = (randint(20, WIDTH-20), randint(20, HEIGHT-20))

def time_up():
    global gameOver
    gameOver = True

def update():
    global score

    spd = 2
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

    fox.x += (moveH/Mag) * spd
    fox.y += (moveV/Mag) * spd

    coin_collected = fox.colliderect(coin)

    if coin_collected:
        score += 10
        place_object(coin)

place_object(coin)
clock.schedule(time_up, 20)