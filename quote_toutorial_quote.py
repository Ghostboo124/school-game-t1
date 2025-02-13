"""
This is a game where you shoot an apple
"""
#import pgzero
from random import randint
import pygame
import quote_toutorial_quote
import time

font = pygame.font.SysFont(None, 24)
apple = Actor("apple")
winCounter = 0
loseCounter = 0

def draw() -> None:
    screen.clear()
    apple.draw()
    t0 = time.time()
    counter1 = quote_toutorial_quote.font.render(f'Win Counter: {quote_toutorial_quote.winCounter}', True, pygame.Color(255,255,255))
    counter2 = quote_toutorial_quote.font.render(f'Lose Counter: {quote_toutorial_quote.loseCounter}', True, pygame.Color(255,255,255))
    print('time needed for Font creation :', time.time()-t0)
    screen.blit(counter1, (10, 10))
    screen.blit(counter2, (10, 30))

def place_apple() -> None:
    #apple.x, apple.y = (768, 565)
    apple.x, apple.y = (randint(35, 768), randint(40, 565))

def on_mouse_down(pos) -> None:
    if apple.collidepoint(pos):
        print('Good Shot!')
        place_apple()
        quote_toutorial_quote.winCounter += 1
    else:
        print("You missed!")
        quote_toutorial_quote.winCounter = 0
        quote_toutorial_quote.loseCounter += 1