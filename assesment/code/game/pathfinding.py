from sys import stderr, exit as __exit
import pygame
import numpy
from queue import PriorityQueue
from pytmx import TiledMap

try:
    from typing import TYPE_CHECKING, Any, Optional
except (ImportError, OSError):
    try:
        stderr.write("Error whilst importing typing!\nFalling back to typing_extensions")
        from typing_extensions import TYPE_CHECKING, Any, Optional
    except ImportError:
        stderr.write("Error has occured whilst importing typing_extensions!")
        __exit(1)

if TYPE_CHECKING:
    from .pathfinding import Spot
else:
    class Spot: pass

def abs(x) -> float:
    return numpy.sqrt(numpy.square(x)) # Returns the square root of the square of x, this makes any negative numbers non-negative and any positive numbers positive

def h(p1: numpy.ndarray[float, float], p2: numpy.ndarray[float, float]) -> float: # type: ignore
    x1, y1 = p1
    x2, y2 = p2
    return abs(x=x1 - x2) + abs(x=y1 - y2)

def reconstructPath(cameFrom: dict, current: Spot) -> list[Spot]:
    path: list[Spot] = []
    while current in cameFrom:
        current = cameFrom[current]
        path.append(current)
    return path

def astar(grid: list[list[Spot]], start: Spot, end: Spot) -> Optional[list[Spot]]:
    count = 0
    openSet = PriorityQueue()
    openSet.put(item=(0, count, start))
    cameFrom: dict[Spot, Any] = {}
    gScore: dict[Spot, float] = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore: dict[Spot, float] = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(p1=start.getPos(), p2=end.getPos())
    openSetHash: set[Spot] = {start}

    while not openSet.empty():
        current: Spot = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            return reconstructPath(cameFrom=cameFrom, current=end)
        
        for neighbor in current.neighbors:
            tempGscore: float = gScore[current] + 1
            if tempGscore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGscore
                fScore[neighbor] = tempGscore + h(p1=neighbor.getPos(), p2=end.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put(item=(fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
    return None

class Spot:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row: int = row
        self.col: int = col
        self.x: int = row * width
        self.y: int = col * width
        self.color: tuple[int, int, int] = (255, 255, 255)  # White
        self.neighbors: list[Spot] = []
        self.width: list = width
        self.total_rows: int = total_rows

    def getPos(self) -> numpy.ndarray:
        return numpy.array((self.x, self.y), float)

    def isBarrier(self) -> bool:
        return self.color == (0, 0, 0)  # Black

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

def createGrid(mapData: TiledMap) -> list[list[Spot]]:
    grid: list[list[Spot]] = []
    tileWidth: int = mapData.tilewidth
    tileHeight: int = mapData.tileheight
    mapWidth: int = mapData.width
    mapHeight: int = mapData.height
    print(f"{mapWidth=}, {mapHeight=}")
    # for tileX in range(max(0, startX), min(endX, mapWidth)):
    #     for tileY in range(max(0, startY), min(endY, mapHeight)):
    #         tileIndex: int = tileY * mapWidth + tileX
    #         if tileIndex < len(layer.data) and layer.data[tileIndex] != 0:
    #             tileRect = pygame.Rect(tileX * tileWidth, tileY * tileHeight, tileWidth, tileHeight)
    #             if actorRect.colliderect(tileRect):
    #                 return True
    for row in range(tileHeight):
        grid.append([])
        for col in range(mapWidth):
            spot = Spot(row=row, col=col, width=tileWidth, total_rows=mapHeight)
            tileIndex: int = col + row * tileWidth
            for layer in mapData.visible_layers:
                if hasattr(layer, "data"):
                    spot.color = (0, 0, 0)
            grid[row].append(spot)
    return grid

def updateNeighbors(grid: list[list[Spot]]) -> None:
    for row in grid:
        for spot in row:
            spot.updateNeighbors(grid=grid)