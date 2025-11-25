# MazeFun

A collection of Python scripts to visualize the generation and solving of mazes using **Pygame**. This is the code for this [youtube video](https://www.youtube.com/watch?v=4L7BDRmH4cM).

![Maze](./images/examples/smallRACE_MazeDijkstra2023-12-22_13-04-44.png)

## requirements

You will need Python 3 installed along with the following libraries:

```bash
pip install pygame networkx
```

*Note: `ffmpeg` is required if you wish to use the video creation script.*

## how to Run

The project is split into two phases: **Generation** and **Solving**.

### 1. generate a Maze

Run one of the generation scripts to create a maze. This will visualize the process and save a `.dat` file to the `./mazes/` directory.

  * `python recursiveBackTracker.py` (Recursive Backtracker)
  * `python primsAlgorithm.py` (Prim's Algorithm)
  * `python wilsonAlgorithm.py` (Wilson's Algorithm)

### 2. solve the Maze

Once a maze is generated, run the solver script.

  * `python solvingAlgorithms.py`

**Important:** Ensure the `MAZE_NAME` variable in `solvingAlgorithms.py` matches the name of the maze you generated (e.g., `"primsMaze.dat"`).

### 3. create a Video (Optional)

If you enabled image saving in the solver, you can stitch them into a video:

  * `python movieMake.py`

## configuration

You can tweak settings directly inside the Python files (look for the "CHANGE THIS" comments):

  * **Dimensions:** Change `WIDTH` and `HEIGHT` to adjust grid size.
  * **Speed:** Change `DELAY` (or set to `False`) to speed up visualizations.
  * **Algorithms:** In `solvingAlgorithms.py`, modify the `RUN` dictionary to toggle specific solvers (e.g., set `"dijkstra": True`).

## output

The scripts automatically generate the following folders for outputs:

  * `/mazes`: Stores the serialized maze data (`.dat`).
  * `/images`: Stores screenshots of the finished mazes.
  * `/video`: Stores frame sequences for video creation.