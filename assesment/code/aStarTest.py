import pygame
import math
import numpy
from random import randint
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)



def abs(n: float | int) -> float | int:
    """
    Returns the absolute value
    Args:
        n: The number to get the absolute value of, int or float
    """
    return numpy.sqrt(numpy.square(n)) # return the square root of the square on n

class Spot:
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def __lt__(self, other):
        return False

    def getPos(self) -> tuple:
        return (self.row, self.col)

    def isClosed(self) -> bool:
        return self.color == RED

    def isOpen(self) -> bool:
        return self.color == GREEN

    def isBarrier(self) -> bool:
        return self.color == BLACK

    def isStart(self) -> bool:
        return self.color == ORANGE

    def isEnd(self) -> bool:
        return self.color == TURQUOISE

    def reset(self) -> None:
        self.color = WHITE

    def makeStart(self) -> None:
        self.color = ORANGE

    def makeClosed(self)-> None:
        self.color = RED

    def makeOpen(self) -> None:
        self.color = GREEN

    def makeBarrier(self) -> None:
        self.color = BLACK

    def makeEnd(self) -> None:
        self.color = TURQUOISE

    def makePath(self) -> None:
        self.color = PURPLE

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid) -> None:
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1: tuple, p2: tuple) -> float:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstructPath(cameFrom: dict, current: Spot, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()

def astar(draw, grid: list, start: Spot, end: Spot):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPos(), start.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            reconstructPath(cameFrom, end, draw)
            end.makeEnd()
            return True
        
        for neighbor in current.neighbors:
            tempGscore = gScore[current] + 1
            if tempGscore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGscore
                fScore[neighbor] = tempGscore + h(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        
        draw()

        if current != start:
            current.makeClosed()

    return False

def makeGrid(rows: int, width: int) -> tuple[list, Spot, Spot]:
    """
    A Function to make a grid, returns a list of the grid
    Args:
        rows: The number of rows in the grid, intiger
    """
    grid = []
    gap = width // rows
    end = False
    start = False
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            number = randint(0, 255)
            if number <= 5 and start == False:
                spot.makeStart()
                start = spot
            elif number <= 70:
                spot.makeBarrier()
            elif number <= 245:
                spot.reset()
            elif number <= 250 and end == False:
                spot.makeEnd()
                end = spot
            else:
                spot.reset()
            grid[i].append(spot)
    
    if end == False:
        end = grid[rows-5][width-1]
        end.makeEnd()
    if start == False:
        start = grid[rows-1][width-5]
        start.makeStart()
        
    return (grid, start, end)

def drawGrid(win: pygame.Surface, rows: int, width: int) -> None:
    """
    A Function to draw the grid
    Args:
        win: The window to draw it to, pygame.surface
        rows: The number of rows in the grid, integer
        width: The width of the grid, integer
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win: pygame.Surface, grid: list, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    drawGrid(win, rows, width)
    pygame.display.update()

def getClickedPos(pos: tuple[int, int], rows: int, width: int) -> tuple:
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    
    return (row, col)

def main(win: pygame.Surface, width: int):
    ROWS = 50
    grid, start, end = makeGrid(ROWS, width)
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: # Left
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makeStart()
                elif not end and spot != start:
                    end = spot
                    end.makeEnd()
                elif spot != end and spot != start:
                    spot.makeBarrier()
            if pygame.mouse.get_pressed()[2]: # Right
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                    
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid, start, end = makeGrid(ROWS, width)

main(WIN, WIDTH)
pygame.quit()
exit(0)