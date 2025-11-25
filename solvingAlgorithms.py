import pygame
import sys
import random
import time
import pickle
import copy
import networkx as nx
import os
from datetime import datetime

# CHANGE - YOU CAN CHANGE THIS!!!! 
WIDTH, HEIGHT = 100*2*3, 100*2*3 # Make sure it's
W = 5*2*3 # Normally I set it to 5
RUN = {
    "randomMouseAlgorithm": False,
    "wallFollower": True,
    "wallFollowerLeft": False,
    "deadEndFillings": False,
    "dijkstra": False,
    "aStar": False
}
MAZE_NAME = "primsMaze.dat"
SHOW = True
OUTPUT_IMAGE = True
OUTPUT_IMAGE_NAME = "mazePatreonsAreAwesome2"
SAVE_VIDEO = True
DELAY = False

# Constants
ROWS = HEIGHT // W
COLS = WIDTH // W
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
DARK_RED = (100, 0, 0)
RED = (255, 0, 0)
outlineThickness = W // 5
hW = W // 2
T = outlineThickness//2

WIDTH, HEIGHT = WIDTH+W, HEIGHT+W,

def load_data():
    with open(f"./mazes/{MAZE_NAME}", 'rb') as f:
        x = pickle.load(f)
    return x

cells = []
wallList = []

pygame.init()
if SHOW:
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
else:
    SCREEN = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('💚💚💚')

def returnCellIndex(row, col):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    else:
        return cells[row][col]

def returnCellIndex_LastPosition(row, col, lastPosition):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    elif row == lastPosition[0] and col == lastPosition[1]:
        return False
    else:
        return cells[row][col]

def returnCellIndex_DeadEndFillings(row, col, arr):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    else:
        return arr[row][col]

class Cell:
    def __init__(self, row, col, lines, inPath, inMaze, highlighted, arrows):
        self.row = row
        self.col = col
        self.lines = lines
        self.inPath = inPath
        self.inMaze = inMaze
        self.highlighted = highlighted
        self.arrows = arrows

    def draw(self):
        if self.inMaze:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.highlighted:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.inPath:
            pygame.draw.rect(SCREEN, DARK_RED, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.lines[0]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W, self.row*W+W+T), outlineThickness)
        if self.lines[1]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W+W), (self.col*W+W+T, self.row*W+W), outlineThickness)
        if self.lines[2]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W+W, self.row*W), (self.col*W+W, self.row*W+W+T), outlineThickness)
        if self.lines[3]:
            pygame.draw.line(SCREEN, GREEN, (self.col*W, self.row*W), (self.col*W+W+T, self.row*W), outlineThickness)
        if self.arrows[0]:
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W, self.row*W+hW), outlineThickness)
        if self.arrows[1]:
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW, self.row*W+hW+hW), outlineThickness)
        if self.arrows[2]:
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW+hW, self.row*W+hW), outlineThickness)
        if self.arrows[3]:
            pygame.draw.line(SCREEN, DARK_RED, (self.col*W+hW, self.row*W+hW), (self.col*W+hW, self.row*W), outlineThickness)
    
    def checkNearCells(self, lastPosition):
        nearCells = []
        printCells = []

        # print(f"Last position: {lastPosition}")
        topCell = returnCellIndex(self.row-1, self.col, lastPosition)
        rightCell = returnCellIndex(self.row, self.col+1, lastPosition)
        bottomCell = returnCellIndex(self.row+1, self.col, lastPosition)
        leftCell = returnCellIndex(self.row, self.col-1, lastPosition)

        if topCell!=False:
            nearCells.append(topCell)
            printCells.append(["TopCell", [topCell.row, topCell.col]])

        if rightCell!=False:
            nearCells.append(rightCell)
            printCells.append(["RightCell", [rightCell.row, rightCell.col]])

        if bottomCell!=False:
            nearCells.append(bottomCell)
            printCells.append(["BottomCell", [bottomCell.row, bottomCell.col]])

        if leftCell!=False:
            nearCells.append(leftCell)
            printCells.append(["LeftCell", [leftCell.row, leftCell.col]])
        
        # print(f"Len NearCells: {printCells}")
        
        if len(nearCells) != 0:
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
        else:
            pass

    def checkNextCells(self, lastPosition):
        print(self.lines)
        nearCells = []
        printCells = []

        # print(f"Last position: {lastPosition}")
        topCell = returnCellIndex(self.row-1, self.col)
        rightCell = returnCellIndex(self.row, self.col+1)
        bottomCell = returnCellIndex(self.row+1, self.col)
        leftCell = returnCellIndex(self.row, self.col-1)

        if topCell!=False and not(self.lines[3]):
            nearCells.append(topCell)
            printCells.append(["TopCell", [topCell.row, topCell.col]])

        if rightCell!=False and not(self.lines[2]):
            nearCells.append(rightCell)
            printCells.append(["RightCell", [rightCell.row, rightCell.col]])

        if bottomCell!=False and not(self.lines[1]):
            nearCells.append(bottomCell)
            printCells.append(["BottomCell", [bottomCell.row, bottomCell.col]])

        if leftCell!=False and not(self.lines[0]):
            nearCells.append(leftCell)
            printCells.append(["LeftCell", [leftCell.row, leftCell.col]])
        
        if len(nearCells) != 0:
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
        else:
            return cells[lastPosition[0]][lastPosition[1]]
    
    def checkNearCell_DeadEnd(self, arr):
        nearCells = []
        printCells = []

        topCell = returnCellIndex_DeadEndFillings(self.row-1, self.col, arr)
        rightCell = returnCellIndex_DeadEndFillings(self.row, self.col+1, arr)
        bottomCell = returnCellIndex_DeadEndFillings(self.row+1, self.col, arr)
        leftCell = returnCellIndex_DeadEndFillings(self.row, self.col-1, arr)

        if topCell!=False and not(self.lines[3]):
            nearCells.append(topCell)
            printCells.append(["TopCell", [topCell.row, topCell.col]])

        if rightCell!=False and not(self.lines[2]):
            nearCells.append(rightCell)
            printCells.append(["RightCell", [rightCell.row, rightCell.col]])

        if bottomCell!=False and not(self.lines[1]):
            nearCells.append(bottomCell)
            printCells.append(["BottomCell", [bottomCell.row, bottomCell.col]])

        if leftCell!=False and not(self.lines[0]):
            nearCells.append(leftCell)
            printCells.append(["LeftCell", [leftCell.row, leftCell.col]])
        
        
        if len(nearCells) != 0:
            if len(nearCells) == 1:
                return nearCells[0]
            else:
                return False
        else:
            return False

def deleteWalls(currentCell, nextCell):
    x = currentCell.row - nextCell.row

    if x == 1:
        currentCell.lines[3] = False
        nextCell.lines[1] = False
    elif x == -1:
        currentCell.lines[1] = False
        nextCell.lines[3] = False

    y = currentCell.col - nextCell.col
    if y == 1:
        currentCell.lines[0] = False
        nextCell.lines[2] = False
    elif y == -1:
        currentCell.lines[2] = False
        nextCell.lines[0] = False

def setUp():
    print("")
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cells[i].append(Cell(i,j, [True, True, True, True], False, False, False))

def eraseWrongPath(arr, target_object):
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].inPath = False
    
    newArray = []
    aux = True
    for idx, cell in enumerate(arr):
        if aux == True:
            if cell == target_object:
                newArray.append(cell)
                aux = False
            elif cell != target_object:
                newArray.append(cell)
    
    for i in range(ROWS):
        for j in range(COLS):
            if cells[i][j] in newArray:
                cells[i][j].inPath = True
    return newArray

def showPath(pathSolution, way, name="Unnamed"):
    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if way == "Easy":
        for cell in pathSolution:
            cell.inPath = True
    
    elif way == "Hard":
        for idx, cell in enumerate(pathSolution):
            if idx < len(pathSolution)-1:
                currentCell = pathSolution[idx]
                nextCell = pathSolution[idx+1]

                x = nextCell.row - currentCell.row

                if x == 1:
                    currentCell.arrows[1] = True
                    nextCell.arrows[3] = True
                elif x == -1:
                    currentCell.arrows[3] = True
                    nextCell.arrows[1] = True

                y = nextCell.col - currentCell.col
                if y == 1:
                    currentCell.arrows[2] = True
                    nextCell.arrows[0] = True
                elif y == -1:
                    currentCell.arrows[2] = True
                    nextCell.arrows[0] = True
    updateCanvas()

def updateCanvas():
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    if SHOW:
        pygame.display.update()

def checkWalls(arr1, arr2):
    directionIndex = arr1.index(1)
    newArray = arr2

    for i in range(directionIndex):
        a = newArray[0]
        newArray.pop(0)
        newArray.extend([a])
    
    return newArray

def checkWallsLeft(arr1, arr2):
    directionIndex = arr1.index(1)
    newArray = arr2

    for i in range(directionIndex):
        a = newArray[(len(newArray)-1)]
        newArray.pop((len(newArray)-1))
        newArray.insert(0, a)
    
    return newArray

def moveForward(current, direction):
    current.inMaze = True
    directionIndex = direction.index(1)
    row = current.row
    col = current.col

    if directionIndex == 0:
        return cells[row][col-1]
    elif directionIndex == 1:
        return cells[row+1][col]
    elif directionIndex == 2:
        return cells[row][col+1]
    elif directionIndex == 3:
        return cells[row-1][col]
    else:
        print("Something Went Wrong")
        return False

def fillWalls(cell, arr):
     
    topCell = returnCellIndex_DeadEndFillings(cell.row-1, cell.col, arr)
    rightCell = returnCellIndex_DeadEndFillings(cell.row, cell.col+1, arr)
    bottomCell = returnCellIndex_DeadEndFillings(cell.row+1, cell.col, arr)
    leftCell = returnCellIndex_DeadEndFillings(cell.row, cell.col-1, arr)

    if topCell != False:
        topCell.lines[1] = True
    if rightCell != False:
        rightCell.lines[0] = True
    if bottomCell != False:
        bottomCell.lines[3] = True
    if leftCell != False:
        leftCell.lines[2] = True

def clearScreen(arr):
    SCREEN.fill(BLACK)

    for i in range(ROWS):
        for j in range(COLS):
            arr[i][j].inMaze = False
            arr[i][j].inPath = False
            arr[i][j].highlighted = False
    updateCanvas()

def addZeros(number, desired_length):
    number_str = str(number)
    zeros_to_add = max(0, desired_length - len(number_str))
    if number_str.startswith('-'):
        return '-' + '0' * zeros_to_add + number_str[1:]
    else:
        return '0' * zeros_to_add + number_str

def randomMouseAlgorithm(startCell, endCell, show, delay=False):
    done = False
    path = []

    current = startCell
    current.highlighted = True
    path.append(current)
    lastPosition = [current.row, current.col]
    
    while not(done):
        if show:
            updateCanvas()

        next = current.checkNextCells(lastPosition)
        
        if next == endCell:
            done = False
            return path
        else:
            current.inMaze = True
            current.highlighted = False
            current = next
            current.highlighted = True
            path.append(current)
            if len(path) > 1:
                lastPosition = [path[-2].row, path[-2].col]
            else:
                lastPosition = [path[-1].row, path[-1].col]
        if delay:
            time.sleep(delay)
    path = list(dict.fromkeys(path))
    return path

def wallFollower(startCell, endCell, show, saveVideo=False, delay=False):
    global MAZE_NAME
    done = False
    path = [startCell]
    direction = [1, 0, 0, 0]

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    current = startCell
    current.highlighted = True
    path.append(current)

    bestPosition = [current.row,current.col]

    i = 0
    k=0
    while not(done):
        def showUpdate(k):
            if show:
                updateCanvas()
                if saveVideo:

                    directory = f"./video/wallFollower{MAZE_NAME}{current_date_time}/"

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")

                    else:
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")

        nextWalls = checkWalls(direction, list(current.lines))
        
        if nextWalls[1] == True:
            if nextWalls[0] == True:
                tmpValue = direction[0]
                direction.pop(0)
                direction.extend([tmpValue])
    
            else:
                showUpdate(k)
                k+=1

                next = moveForward(current, direction)
                current.highlighted = False
                next.highlighted = True
                current = next
                path.append(current)
        else:
            tmpValue = direction[(len(direction)-1)]
            direction.pop((len(direction)-1))
            direction.insert(0, tmpValue)

            showUpdate(k)
            k+=1

            # Move Forward
            next = moveForward(current, direction)
            current.highlighted = False
            next.highlighted = True
            current = next
            path.append(current)

        if current == endCell:
            done = False
            return path
        if current == startCell and path != [startCell] and direction != [1, 0, 0, 0] and i > 5:
            done = False
            return False
        i += 1
        if delay:
            time.sleep(delay)
    
        
def wallFollowerLeft(startCell, endCell, show, saveVideo=False, delay=False):
    global MAZE_NAME
    done = False
    path = [startCell]
    direction = [1, 0, 0, 0]

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    current = startCell
    current.highlighted = True
    path.append(current)

    bestPosition = [current.row,current.col]

    i = 0
    k = 0
    while not(done):
        def showUpdate(k):
            if show:
                updateCanvas()
                # time.sleep(0.1)
                if saveVideo:

                    directory = f"./video/wallFollowerLeft{MAZE_NAME}{current_date_time}/"

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")

                    else:
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")


        nextWalls = checkWalls(direction, list(current.lines))
        
        if nextWalls[3] == True:
            if nextWalls[0] == True:
                tmpValue = direction[(len(direction)-1)]
                direction.pop((len(direction)-1))
                direction.insert(0, tmpValue)
                
    
            else:
                showUpdate(k)
                k+=1

                next = moveForward(current, direction)
                current.highlighted = False
                next.highlighted = True
                current = next
                path.append(current)
        else:
            tmpValue = direction[0]
            direction.pop(0)
            direction.extend([tmpValue])

            showUpdate(k)
            k+=1

            # Move Forward
            next = moveForward(current, direction)
            current.highlighted = False
            next.highlighted = True
            current = next
            path.append(current)

        if current == endCell:
            done = False
            return path
        if current == startCell and path != [startCell] and direction != [1, 0, 0, 0] and i > 5:
            print("This Maze Has No Solution")
            done = False
            return False
        i += 1
        if delay:
            time.sleep(delay)

def deadEndFillings(show, saveVideo, delay=False):
    global MAZE_NAME
    # Identify Dead-End Fillings
    deadEnds = []
    path = []

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Change for newCells
    newCells = [copy.deepcopy(cell) for cell in cells]

    startCell = newCells[0][0]
    endCell = newCells[ROWS-1][COLS-1]
    print(f"DeadEndFillings Started: {time.time()}")
    
    for i in range(ROWS):
        for j in range(COLS):
            if newCells[i][j].lines.count(False) == 1 and newCells[i][j] != endCell:
                deadEnds.append(newCells[i][j])
    k = 0
    for deadEnd in deadEnds:
        done = False
        current = deadEnd
        next = current.checkNearCell_DeadEnd(newCells)
        while not(done):
            
            if next == startCell or next == endCell or current == startCell:
                break
            cells[current.row][current.col].highlighted = True
            cells[current.row][current.col].inMaze = True

            if next != False and next.lines.count(False) == 2:
                current.lines = [True, True, True, True]
                fillWalls(current, newCells)
                current.inMaze = True
                cells[current.row][current.col].highlighted = False
                current = next
            else:
                done = True
                current.lines = [True, True, True, True]
                fillWalls(current, newCells)
                current.inMaze = True
            
            next = current.checkNearCell_DeadEnd(newCells)
            
            if show:
                updateCanvas()
                if saveVideo:

                    directory = f"./video/deadEndFillings{MAZE_NAME}{current_date_time}/"

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                        k += 1

                    else:
                        pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                        k += 1

                    
            cells[current.row][current.col].highlighted = False
            if delay:
                time.sleep(delay)
    
    for i in range(ROWS):
        for j in range(COLS):
            if newCells[i][j].inMaze == False:
                path.append(cells[i][j])
    return path
            
def dijkstra(startCell, endCell, show, saveVideo=False, delay=False):
    global MAZE_NAME
    G = nx.Graph()
    nodes = []
    for i in range(ROWS):
        for j in range(COLS):
            nodes.append((i, j))
    
    for i in range(ROWS):
        for j in range(COLS):
            if cells[i][j].lines[0] == False and returnCellIndex(i, j-1) != False:
                G.add_edge((i,j), (i,j-1), weight=1)
            if cells[i][j].lines[1] == False and returnCellIndex(i+1, j) != False:
                G.add_edge((i,j), (i+1,j), weight=1)
            if cells[i][j].lines[2] == False and returnCellIndex(i, j+1) != False:
                G.add_edge((i,j), (i,j+1), weight=1)
            if cells[i][j].lines[3] == False and returnCellIndex(i-1, j) != False:
                G.add_edge((i,j), (i-1,j), weight=1)

    start = (startCell.row, startCell.col)
    end = (endCell.row, endCell.col)

    explored_cells = []

    def explore_cell(node):
        cells[node[0]][node[1]].inMaze = True

    distances = {node: float('inf') for node in G.nodes}
    distances[start] = 0

    previous = {node: None for node in G.nodes}

    unvisited_nodes = list(G.nodes)

    bestPosition = [startCell.row,startCell.col]

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    k = 0
    while unvisited_nodes:
        unvisited_nodes.sort(key=lambda node: distances[node])

        current_node = unvisited_nodes.pop(0)

        if current_node == end:
            break

        for neighbor in G.neighbors(current_node):
            tentative_distance = distances[current_node] + G[current_node][neighbor]['weight']

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                previous[neighbor] = current_node

        explore_cell(current_node)
        if show:
            updateCanvas()
            if saveVideo:
                directory = f"./video/dijkstra{MAZE_NAME}{current_date_time}/"

                if not os.path.exists(directory):
                    os.makedirs(directory)
                    pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                    k += 1

                else:
                    pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                    k += 1
        if delay:
            time.sleep(delay)

    shortest_path = [cells[end[0]][end[1]]]
    while end != start:
        end = previous[end]
        shortest_path.append(cells[end[0]][end[1]])

    shortest_path = list(reversed(shortest_path))
    return shortest_path

def aStar(startCell, endCell, show, saveVideo=False, delay=False):
    global MAZE_NAME
    # Create a graph
    G = nx.Graph()
    nodes = []
    for i in range(ROWS):
        for j in range(COLS):
            nodes.append((i, j))
    
    for i in range(ROWS):
        for j in range(COLS):
            if cells[i][j].lines[0] == False and returnCellIndex(i, j-1) != False:
                G.add_edge((i,j), (i,j-1), weight=1)
            if cells[i][j].lines[1] == False and returnCellIndex(i+1, j) != False:
                G.add_edge((i,j), (i+1,j), weight=1)
            if cells[i][j].lines[2] == False and returnCellIndex(i, j+1) != False:
                G.add_edge((i,j), (i,j+1), weight=1)
            if cells[i][j].lines[3] == False and returnCellIndex(i-1, j) != False:
                G.add_edge((i,j), (i-1,j), weight=1)
    # Find the shortest path using Dijkstra's algorithm
    start = (startCell.row, startCell.col)
    end = (endCell.row, endCell.col)

    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    # Create a list to store the explored cells
    explored_cells = []

    def explore_cell(node):
        cells[node[0]][node[1]].inMaze = True

    # Initialize a dictionary to store the distances
    distances = {node: float('inf') for node in G.nodes}
    distances[start] = 0

    # Initialize the previous node dictionary
    previous = {node: None for node in G.nodes}

    # Create a list to store unvisited nodes
    unvisited_nodes = list(G.nodes)

    # Initialize a dictionary to store the costs
    costs = {node: float('inf') for node in G.nodes}
    costs[start] = 0

    # Create a closed set (a set) to store visited nodes
    closed_set = set()

    current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    k = 0
    while unvisited_nodes:
        # Sort nodes by cost (g(n) + h(n))
        unvisited_nodes.sort(key=lambda node: costs[node] + heuristic(node, end))

        # Get the node with the smallest cost
        current_node = unvisited_nodes.pop(0)

        if current_node == end:
            break
    
        closed_set.add(current_node)

        for neighbor in G.neighbors(current_node):
            tentative_cost = costs[current_node] + G[current_node][neighbor]['weight']

            if tentative_cost < costs[neighbor]:
                costs[neighbor] = tentative_cost

        explore_cell(current_node)
        closed_set.add(current_node)
        if show:
            updateCanvas()
            if saveVideo:

                directory = f"./video/aStar{MAZE_NAME}{current_date_time}/"

                if not os.path.exists(directory):
                    os.makedirs(directory)
                    pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                    k += 1

                else:
                    pygame.image.save(SCREEN, f"{directory}/{addZeros(k, 8)}.png")
                    k += 1
        if delay:
            time.sleep(delay)

    shortest_path = [cells[end[0]][end[1]]]
    while end != start:
        neighbors = list(G.neighbors(end))
        best_neighbor = min(neighbors, key=lambda node: costs[node] )
        end = best_neighbor
        shortest_path.append(cells[end[0]][end[1]])

    shortest_path = list(reversed(shortest_path))
    return shortest_path


def main():
    global SHOW
    global OUTPUT_IMAGE
    global MAZE_NAME
    global DELAY

    updateCanvas()
    print("MAZE ALGORITHM STARTED")
    start = time.time()

    startCell = cells[0][0]
    endCell = cells[ROWS-1][COLS-1]

    for algorithm in RUN.items():
        if algorithm[0] == "randomMouseAlgorithm" and algorithm[1] == True:
            solution = randomMouseAlgorithm(startCell, endCell, show=SHOW, delay=DELAY)

        elif algorithm[0] == "wallFollower" and algorithm[1] == True:
            solution = wallFollower(startCell, endCell, show=SHOW, saveVideo=SAVE_VIDEO, delay=DELAY)

        elif algorithm[0] == "wallFollowerLeft" and algorithm[1] == True:
            solution = wallFollowerLeft(startCell, endCell, show=SHOW, saveVideo=SAVE_VIDEO, delay=DELAY)

        elif algorithm[0] == "deadEndFillings" and algorithm[1] == True:
            print(SHOW)
            solution = deadEndFillings(show=SHOW,saveVideo=SAVE_VIDEO, delay=DELAY)

        elif algorithm[0] == "dijkstra" and algorithm[1] == True:
            solution = dijkstra(startCell, endCell, show=SHOW, saveVideo=SAVE_VIDEO, delay=DELAY)

        elif algorithm[0] == "aStar" and algorithm[1] == True:
            solution = aStar(startCell, endCell, show=SHOW, saveVideo=SAVE_VIDEO, delay=DELAY)

    showPath(solution, "Easy", name="smallRACE_MazeWallFollowerLeft")

    end = time.time()
    print(f"Total Time Elapsed: {(end - start)}")
    print("MAZE ALGORITHM FINISHED")
    
    updateCanvas()

    if OUTPUT_IMAGE:
        current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print("Saving Image!")
        pygame.image.save(SCREEN, f"./images/{OUTPUT_IMAGE_NAME}{current_date_time}.png")
        print("Image saved!")
   
    
cells = load_data()

print(f"Len cells: {len(cells)}")
print(f"Len cells: {len(cells[0])}")

for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].inMaze = False

start = time.time()
main()
end = time.time()
print(f"Total Time Elapsed: {(end - start)}")