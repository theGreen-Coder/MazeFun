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
MAZE_NAME = "primsMaze"
DELAY = 0.01

# CONSTANTS
ROWS = HEIGHT // W
COLS = WIDTH // W
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
outlineThickness = W // 5
T = outlineThickness//2
k = 0

WIDTH, HEIGHT = HEIGHT+W, WIDTH+W

print(f"Number of Cells: {ROWS}")
print(f"Surface Area: {ROWS*COLS}")

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

def addZeros(number, desired_length):
    # Convert the number to a string
    number_str = str(number)

    # Calculate the number of zeros to add
    zeros_to_add = max(0, desired_length - len(number_str))

    # Check if the number is negative
    if number_str.startswith('-'):
        # If it's negative, add zeros after the negative sign
        return '-' + '0' * zeros_to_add + number_str[1:]
    else:
        # If it's positive, simply add zeros to the beginning
        return '0' * zeros_to_add + number_str

def updateCanvas():
    SCREEN.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].draw()
    if SHOW:
        pygame.display.update()

def deleteWalls(currentCell, nextCell):
    global k
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


def main():
    global SHOW
    global SAVE_MAZE
    global OUTPUT_IMAGE
    global MAZE_NAME
    global DELAY
    setUp()

    firstCell = cells[0][0]
    firstCell.inMaze = True

    wallList.append([firstCell, 0])
    wallList.append([firstCell, 1])
    wallList.append([firstCell, 2])
    wallList.append([firstCell, 3])


    running = True
    print("MAZE ALGORITHM STARTED")
    while running:
        
        while len(wallList) > 0:
            randomWall = random.choice(wallList)
            if DELAY:
                time.sleep(DELAY)

            if randomWall[1] == 0 and returnCellIndex(randomWall[0].row-1, randomWall[0].col) != False:
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex-1][colIndex]

                if randomWall[0].inMaze ^ dividingCell.inMaze:
                    deleteWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].inMaze):
                        randomWall[0].inMaze = True
                    if not(dividingCell.inMaze):
                        dividingCell.inMaze = True
                        wallList.append([dividingCell, 0])
                        wallList.append([dividingCell, 1])
                        wallList.append([dividingCell, 3])
            
            if randomWall[1] == 1 and returnCellIndex(randomWall[0].row, randomWall[0].col+1) != False:
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex][colIndex+1]

                if randomWall[0].inMaze ^ dividingCell.inMaze:
                    deleteWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].inMaze):
                        randomWall[0].inMaze = True
                    if not(dividingCell.inMaze):
                        dividingCell.inMaze = True
                        wallList.append([dividingCell, 0])
                        wallList.append([dividingCell, 1])
                        wallList.append([dividingCell, 2])

            if randomWall[1] == 2 and returnCellIndex(randomWall[0].row+1, randomWall[0].col) != False:
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex+1][colIndex]

                if randomWall[0].inMaze ^ dividingCell.inMaze:
                    deleteWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].inMaze):
                        randomWall[0].inMaze = True
                    if not(dividingCell.inMaze):
                        dividingCell.inMaze = True
                        wallList.append([dividingCell, 1])
                        wallList.append([dividingCell, 2])
                        wallList.append([dividingCell, 3])
            
            if randomWall[1] == 3 and returnCellIndex(randomWall[0].row, randomWall[0].col-1) != False:
                rowIndex = randomWall[0].row
                colIndex = randomWall[0].col
                dividingCell = cells[rowIndex][colIndex-1]

                if randomWall[0].inMaze ^ dividingCell.inMaze:
                    deleteWalls(randomWall[0], dividingCell)

                    if not(randomWall[0].inMaze):
                        randomWall[0].inMaze = True
                    if not(dividingCell.inMaze):
                        dividingCell.inMaze = True
                        wallList.append([dividingCell, 0])
                        wallList.append([dividingCell, 2])
                        wallList.append([dividingCell, 3])

            wallList.remove(randomWall)
        


            if SHOW:
                updateCanvas()
        

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
        break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
   
    
start = time.time()
main()
end = time.time()
print(f"Total Time Elapsed: {(end - start)}")