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
highScore = 0
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
            place_object(apple)
            place_object(pineapple)
            place_object(orange)
        variables.start = False
    screen.clear()
    apple.draw()
    pineapple.draw()
    orange.draw()
    t0 = time.time()
    counter1 = variables.font.render(f'Win Counter: {variables.winCounter}', True, pygame.Color(255,255,255))
    counter2 = variables.font.render(f'Lose Counter: {variables.loseCounter}', True, pygame.Color(255,255,255))
    counter3 = variables.font.render(f'High Score: {variables.highScore}', True, pygame.Color(255,255,255))
    print('time needed for Font creation :', time.time()-t0)
    screen.blit(counter1, (10, 10))
    screen.blit(counter2, (10, 30)) 
    screen.blit(counter3, (10, 50))

def on_mouse_down(pos) -> None:
    if apple.collidepoint(pos):
        print('Good Shot!')
        place_object(apple)
        variables.winCounter += 1
        if variables.winCounter > variables.highScore:
            print("You beat your high score!")
            variables.highScore = variables.winCounter
        
    elif pineapple.collidepoint(pos):
        print('Good Shot!')
        place_object(pineapple)
        variables.winCounter += 1
        if variables.winCounter > variables.highScore:
            print("You beat your high score!")
            variables.highScore = variables.winCounter
    elif orange.collidepoint(pos):
        print('Good Shot!')
        place_object(orange)
        variables.winCounter += 1
        if variables.winCounter > variables.highScore:
            print("You beat your high score!")
            variables.highScore = variables.winCounter
    else:
        print("You missed!")
        variables.winCounter = 0    
        variables.loseCounter += 1 