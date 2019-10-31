"""
Basic block maze generator found online
https://en.wikipedia.org/wiki/Maze_generation_algorithm#Python_code_example
"""

import numpy
from numpy.random import randint as rand
#pylint: disable=all
class Maze:
    def __init__(self, w=81, h=51, complexity=.75, density=.75):
        self.width = w
        self.height = h
        self.complexity = complexity
        self.density = density
        self.maze = None

    def generate_maze(self):
        # Only odd shapes
        shape = ((self.height // 2) * 2 + 1, (self.width // 2) * 2 + 1)
        # Adjust complexity and density relative to maze size
        complexity = int(self.complexity * (5 * (shape[0] + shape[1]))) # number of components
        density    = int(self.density * ((shape[0] // 2) * (shape[1] // 2))) # size of components
        # Build actual maze
        Z = numpy.zeros(shape, dtype=bool)
        # Fill borders
        Z[0, :] = Z[-1, :] = 1
        Z[:, 0] = Z[:, -1] = 1
        # Make aisles
        for _ in range(density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2 # pick a random position
            Z[y, x] = 1
            for _ in range(complexity):
                neighbours = []
                if x > 1:             neighbours.append((y, x - 2))
                if x < shape[1] - 2:  neighbours.append((y, x + 2))
                if y > 1:             neighbours.append((y - 2, x))
                if y < shape[0] - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                    if Z[y_, x_] == 0:
                        Z[y_, x_] = 1
                        Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_
        self.maze = Z
        return Z
