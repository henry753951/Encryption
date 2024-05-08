import random
import os

LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3


class Maze:
    class Cell:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y
            self.cheese = False
            self.visited = False
            self.start = False
            self.walls = [True, True, True, True]  # Left, Right, Up, Down

        def getChildren(self, grid: list) -> list:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            children = [
                grid[self.y + dy][self.x + dx]
                for dx, dy in directions
                if 0 <= self.x + dx < len(grid)
                and 0 <= self.y + dy < len(grid)
                and not grid[self.y + dy][self.x + dx].visited
            ]
            return children

    def __init__(self, size: int, cheeses: int):
        self.start_pos = (0, 0)
        self.size = size
        self.grid = [[Maze.Cell(x, y) for x in range(size)] for y in range(size)]
        self.current = self.grid[0][0]
        self.stack = []

        self.__shuffled_map = (
            [1 for _ in range(cheeses)] + [0 for _ in range(size * size - cheeses - 1)] + [2]
        )
        random.shuffle(self.__shuffled_map)

    def removeWalls(self, current: Cell, choice: Cell):
        direction_mapping = {
            (1, 0): (RIGHT, LEFT),
            (-1, 0): (LEFT, RIGHT),
            (0, 1): (DOWN, UP),
            (0, -1): (UP, DOWN),
        }

        dx = choice.x - current.x
        dy = choice.y - current.y
        current_wall, choice_wall = direction_mapping[(dx, dy)]

        current.walls[current_wall] = False
        choice.walls[choice_wall] = False

    def displayMaze(self):
        def drawWalls(binGrid: list) -> list:
            wall_positions = {LEFT: (1, 0), RIGHT: (1, 2), UP: (0, 1), DOWN: (2, 1)}
            for yindex, row in enumerate(self.grid):
                for xindex, cell in enumerate(row):
                    for wall_index, has_wall in enumerate(cell.walls):
                        if has_wall:
                            offset_y, offset_x = wall_positions[wall_index]
                            binGrid[yindex * 2 + offset_y][xindex * 2 + offset_x] = '⬛'
                    if cell.cheese:
                        binGrid[yindex * 2 + 1][xindex * 2 + 1] = '🧀'
                    elif cell.start:
                        binGrid[yindex * 2 + 1][xindex * 2 + 1] = '🐭'
            return binGrid

        def drawBorder(binGrid: list) -> list:
            length = len(binGrid)
            binGrid[0] = binGrid[length - 1] = ['⬛'] * length
            for row in binGrid:
                row[0] = row[length - 1] = '⬛'
            return binGrid

        binGrid = []
        length = len(self.grid) * 2 + 1
        for x in range(length):
            if x % 2 == 0:
                binGrid.append(['⬜' if x % 2 != 0 else '⬛' for x in range(length)])
            else:
                binGrid.append(['⬜'] * length)

        binGrid = drawWalls(binGrid)
        binGrid = drawBorder(binGrid)

        print('\n'.join([''.join(x) for x in binGrid]))

    def generateMaze(self):
        while True:
            self.current.visited = True
            children = self.current.getChildren(self.grid)
            if children:
                choice = random.choice(children)
                choice.visited = True
                temp = self.__shuffled_map.pop()
                if temp == 1:
                    choice.cheese = True
                elif temp == 2:
                    choice.start = True
                    self.start_pos = (choice.x, choice.y)
                self.stack.append(self.current)
                self.removeWalls(self.current, choice)
                self.current = choice
            elif self.stack:
                self.current = self.stack.pop()
            else:
                break

            self.displayMaze()
            os.system('cls')
        return [[list(map(int, cell.walls)) for cell in row] for row in self.grid], [
            [int(cell.cheese) for cell in row] for row in self.grid
        ]


size = int(input('Enter a maze size: '))
maze = Maze(size, cheeses=10)
maze_map, cheese_map = maze.generateMaze()
maze.displayMaze()
key = ''.join(''.join(''.join(str(x) for x in cell) for cell in row) for row in maze_map)
cheese_key = ''.join(''.join(str(x) for x in cell) for cell in cheese_map)
key_len = len(key)
print(f"Key-pairs: {key_len}")
print(f"Key: {int(key, 2)} - {key_len} - {int(cheese_key, 2)}")
print(f"Key: {hex(int(key, 2))}-{hex(key_len)}-{hex(int(cheese_key, 2))}")
