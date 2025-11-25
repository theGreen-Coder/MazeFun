import pygame
import sys
import random
import time
import pickle

# CHANGE - YOU CAN CHANGE THIS!!!! 
WIDTH, HEIGHT = 100*2, 100*2 # CONTROLS the Number of ROWS and COLUMNS
W = 5*2 # Normally I set it to 5
SHOW = True
SAVE_MAZE = True
OUTPUT_IMAGE = True
MAZE_NAME = "wilsonMaze"
DELAY = 0.3

# CONSTANTS
ROWS = HEIGHT // W
COLS = WIDTH // W
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
DARK_RED = (100, 0, 0)
RED = (255, 0, 0)
outlineThickness = W // 5
T = outlineThickness//2
hW = W // 2

WIDTH, HEIGHT = WIDTH+5, HEIGHT+5

cells = []
wallList = []

print(f"Number of Cells: {ROWS}")
print(f"Surface Area: {ROWS*COLS}")

pygame.init()
if SHOW:
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
else:
    SCREEN = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption('💚💚💚')

def returnCellIndex(row, col, lastPosition):
    if row < 0 or col < 0 or row > ROWS-1 or col > COLS-1:
        return False
    elif row == lastPosition[0] and col == lastPosition[1]:
        return False
    else:
        return cells[row][col]

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
        if self.inPath:
            pygame.draw.rect(SCREEN, GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.inMaze:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.col*W, self.row*W, W, W))
        if self.highlighted:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.col*W, self.row*W, W, W))
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
        
        
        if len(nearCells) != 0:
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
        else:
            print("Something Went Wrong!")

def addZeros(number, desired_length):
    number_str = str(number)

    zeros_to_add = max(0, desired_length - len(number_str))

    if number_str.startswith('-'):
        return '-' + '0' * zeros_to_add + number_str[1:]
    else:
        return '0' * zeros_to_add + number_str
    
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
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cells[i].append(Cell(i,j, [True, True, True, True], False, False, False, [False, False, False, False]))

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

def save_data():
    with open(f"./mazes/{MAZE_NAME}.dat", "wb") as f:
        pickle.dump(cells, f)

def updateCanvas():
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    if SHOW:
        pygame.display.update()

def randomWalk(startCell):
    done = False
    path = []

    current = startCell
    current.inPath = True
    current.highlighted = True
    path.append(current)
    lastPosition = [current.row, current.col]
    
    while not(done):
        if SHOW:
            updateCanvas()

        next = current.checkNearCells(lastPosition)

        if next.inPath == True:
            path = eraseWrongPath(path, next)
            current.highlighted = False
            current = next
            current.highlighted = True
        elif next.inMaze == True:
            path.append(next)
            for idx, cell in enumerate(path):
                path[idx].inPath = False
                path[idx].inMaze = True
                if idx < len(path)-1:
                    deleteWalls(path[idx], path[idx+1])
            
            done = True
            current.highlighted = False
            break

        else:
            current.highlighted = False
            current = next
            current.highlighted = True
            current.inPath = True
            path.append(current)
            if len(path) > 1:
                lastPosition = [path[-2].row, path[-2].col]
            else:
                lastPosition = [path[-1].row, path[-1].col]
        



def main():
    global SHOW
    global SAVE_MAZE
    global OUTPUT_IMAGE
    global MAZE_NAME
    global DELAY
    setUp()

    end = cells[(ROWS//2)][(ROWS//2)]
    end.inMaze = True

    print("MAZE ALGORITHM STARTED")
    for i in range(ROWS):
        for j in range(COLS):
            if cells[i][j].inMaze == False:
                randomWalk(cells[i][j])
                if DELAY:
                    time.sleep(DELAY)

    print("MAZE ALGORITHM FINISHED")
    updateCanvas()
    if SAVE_MAZE == True:
        print("Saving Maze!")
        save_data()
        SAVE_MAZE = False
        print("Mazed Saved!")

    if OUTPUT_IMAGE:
        print("Saving Image!")
        pygame.image.save(SCREEN, f"./images/{MAZE_NAME}.png")
        print("Image saved!")

start = time.time()
main()
end = time.time()
print(f"Total Time Elapsed: {(end - start)}")

