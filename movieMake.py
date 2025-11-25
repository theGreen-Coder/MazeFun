import argparse
import os
import subprocess

imagesDirectory = "./video/wallFollowerprimsMaze.dat2024-01-04_16-21-18/"
outputName = "./video/mazeVideoPatreon4"

command = f"ffmpeg -framerate 30 -pattern_type glob -i '{imagesDirectory}*.png' -c:v libx264 -pix_fmt yuv420p {outputName}.mp4"
subprocess.call(command, shell=True)