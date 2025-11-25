import pygame
import sys
import time
import pickle
import random

# CHANGE - YOU CAN CHANGE THIS!!!! 
WIDTH, HEIGHT = 100*3, 100*3 # CONTROLS the Number of ROWS and COLUMNS
W = 5 # Normally I set it to 5
SHOW = False
SAVE_MAZE = True
OUTPUT_IMAGE = True
MAZE_NAME = "recursiveMaze"
DELAY = False

# CONSTANTS
ROWS = HEIGHT // W
COLS = WIDTH // W
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
outlineThickness = W // 5
T = outlineThickness//2

print(f"Number of Cells: {ROWS}")
print(f"Surface Area: {ROWS*COLS}")

WIDTH, HEIGHT = HEIGHT+W, WIDTH+W

cells = []
stack = []

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
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(self.row*W, self.col*W, W, W))
        if self.highlighted:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(self.row*W, self.col*W, W, W))
        if self.lines[0]:
            pygame.draw.line(SCREEN, GREEN, (self.row*W, self.col*W), (self.row*W+W+T, self.col*W), outlineThickness)
        if self.lines[1]:
            pygame.draw.line(SCREEN, GREEN, (self.row*W+W, self.col*W), (self.row*W+W, self.col*W+W+T), outlineThickness)
        if self.lines[2]:
            pygame.draw.line(SCREEN, GREEN, (self.row*W, self.col*W+W), (self.row*W+W+T, self.col*W+W), outlineThickness)
        if self.lines[3]:
            pygame.draw.line(SCREEN, GREEN, (self.row*W, self.col*W), (self.row*W, self.col*W+W+T), outlineThickness)
    
    def checkNearCells(self):
        nearCells = []

        topCell = returnCellIndex(self.row-1, self.col)
        rightCell = returnCellIndex(self.row, self.col+1)
        bottomCell = returnCellIndex(self.row+1, self.col)
        leftCell = returnCellIndex(self.row, self.col-1)

        if topCell!=False and not(topCell.inMaze):
            nearCells.append(topCell)

        if rightCell!=False and not(rightCell.inMaze):
            nearCells.append(rightCell)

        if bottomCell!=False and not(bottomCell.inMaze):
            nearCells.append(bottomCell)

        if leftCell!=False and not(leftCell.inMaze):
            nearCells.append(leftCell)
        
        if len(nearCells) != 0:
            if len(nearCells) > 1:
                return random.choice(nearCells)
            else:
                return nearCells[0]
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

def save_data():
    with open(f"./mazes/{MAZE_NAME}.dat", "wb") as f:
        pickle.dump(cells, f)

def setUp():
    for i in range(ROWS):
        cells.append([])
        for j in range(COLS):
            cells[i].append(Cell(i,j, [True, True, True, True], False, False, False, [False, False, False, False]))

def round_to_tenths(number):
    if number < 10:
        return 10
    else:
        return (number // 10) * 10

def main():
    global SHOW
    global SAVE_MAZE
    global OUTPUT_IMAGE
    global MAZE_NAME
    global DELAY

    setUp()

    current = cells[0][0]
    current.inMaze = True
    current.highlighted = True

    running = True
    print("MAZE ALGORITHM STARTED")
    while running:
        
        next = current.checkNearCells()

        if next != False:
            next.inMaze = True

            stack.append(current)

            deleteWalls(current, next)

            current.highlighted = False
            next.highlighted = True
            
            current = next

        elif len(stack) > 0:
            current.highlighted = False
            current = stack.pop(len(stack)-1)
            current.highlighted = True
        else:
            print("MAZE ALGORITHM FINISHED")
            SCREEN.fill(BLACK)
            for i in range(ROWS):
                for j in range(COLS):
                    cells[i][j].draw()
            if SAVE_MAZE == True:
                print("Saving Maze!")
                save_data()
                SAVE_MAZE = False
                print("Mazed Saved!")

            if OUTPUT_IMAGE:
                print("Saving Image!")
                pygame.image.save(SCREEN, f"./images/{MAZE_NAME}.png")
                print("Image saved!")
            running = False
            break
        
        if SHOW:
            SCREEN.fill(BLACK)
            for i in range(ROWS):
                for j in range(COLS):
                    cells[i][j].draw()
            pygame.display.update()
            if DELAY:
                time.sleep(DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
   
start = time.time()
main()
end = time.time()
print(f"Total Time Elapsed: {(end - start)}")