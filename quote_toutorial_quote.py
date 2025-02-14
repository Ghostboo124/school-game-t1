"""
This is a game where you shoot an apple
"""
#import pgzero
from random import randint
import pygame
import quote_toutorial_quote as variables
import time

font = pygame.font.SysFont(None, 24)
apple = Actor("apple")
pineapple = Actor("pineapple")
orange = Actor("orange")
winCounter = 0
loseCounter = 0
start = True

def place_object(actor) -> None:
    max_attempts = 100  # Maximum number of attempts to place the object without collision
    for _ in range(max_attempts):
        if actor == apple:
            actor.x, actor.y = (randint(35, 768), randint(40, 565))
        elif actor == pineapple:
            actor.x, actor.y = (randint(50,750), randint(80,515))
        elif actor == orange:
            actor.x, actor.y = (randint(50, 750), randint(59,535))
        if not check_collision(actor):
            return
    print(f"Failed to place {actor.image} without collision after {max_attempts} attempts, placing it at (200, 200)")
    actor.x, actor.y = (200, 200)

def check_collision(actor) -> bool:
    if actor != apple and apple.collidepoint((actor.x, actor.y)):
        return True
    if actor != pineapple and pineapple.collidepoint((actor.x, actor.y)):
        return True
    if actor != orange and orange.collidepoint((actor.x, actor.y)):
        return True
    return False

def draw() -> None:
    if variables.start:
        for i in range(0,4):
            place_apple()
            place_pineapple()
            place_orange()
        variables.start = False
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    t0 = time.time()
    counter1 = variables.font.render(f'Win Counter: {variables.winCounter}', True, pygame.Color(255,255,255))
    counter2 = variables.font.render(f'Lose Counter: {variables.loseCounter}', True, pygame.Color(255,255,255))
    print('time needed for Font creation :', time.time()-t0)
    screen.blit(counter1, (10, 10))
    screen.blit(counter2, (10, 30))

def place_apple() -> None:
    apple.x, apple.y = (randint(35, 768), randint(40, 565))
    if orange.collidepoint((apple.x, apple.y)):
        print("Apple has collided with the orange")
        place_apple()
    if pineapple.collidepoint((apple.x, apple.y)):
        print("Apple has collided with the pineapple")
        place_apple()

def place_pineapple() -> None:
    pineapple.x, pineapple.y = (randint(50,750), randint(80,515))
    if orange.collidepoint((pineapple.x, pineapple.y)):
        print("Pineapple has collided with the orange")
        place_pineapple()
    if apple.collidepoint((pineapple.x, pineapple.y)):
        print("Pineapple has collided with the apple")
        place_pineapple()

def place_orange() -> None:
    orange.x, orange.y = (randint(50, 750), randint(59,535))
    if pineapple.collidepoint((orange.x, orange.y)):
        print("Orange has collided with the pineapple")
        place_orange()
    if apple.collidepoint((orange.x, orange.y)):
        print("Orange has collided with the apple")
        place_orange()

def on_mouse_down(pos) -> None:
    if apple.collidepoint(pos):
        print('Good Shot!')
        place_apple()
        variables.winCounter += 1
    elif pineapple.collidepoint(pos):
        print('Good Shot!')
        place_pineapple()
        variables.winCounter += 1
    elif orange.collidepoint(pos):
        print('Good Shot!')
        place_orange()
        variables.winCounter += 1
    else:
        print("You missed!")
        variables.winCounter = 0    
        variables.loseCounter += 1