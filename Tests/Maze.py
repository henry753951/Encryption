import random
import os
import string
import time
import hashlib
import numpy as np
from termcolor import colored

CHEESE, PATH, WALL = 2, 1, 0


class Cell:
    def __init__(self, rng: np.random.Generator):
        self.type = WALL
        self.data = {
            "visited_times": 0,
            "random_code": rng.choice(
                list(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            ),
        }


def get_on_color_by_visited_times(visited_times: int):
    visited_times = visited_times % 6
    if visited_times == 1:
        return "on_green"
    elif visited_times == 2:
        return "on_yellow"
    elif visited_times == 3:
        return "on_blue"
    elif visited_times == 4:
        return "on_magenta"
    elif visited_times == 5:
        return "on_cyan"


class MazeSolver:
    x, y = 0, 0

class MazeGenerator:
    def __init__(self, width: int, height: int, cheese_count: int, key: str):
        self.sha_key = int(hashlib.sha256(key.encode()).digest().hex(), 16)
        self.rng = {
            "map": np.random.default_rng(self.sha_key),
            "position": np.random.default_rng(self.sha_key + 1),
            "cell": np.random.default_rng(self.sha_key + 2),
            "direction": np.random.default_rng(self.sha_key + 3),
        }
        os.system("pause")
        self.width = (width if width % 2 != 0 else width + 1) + 2
        self.height = (height if height % 2 != 0 else height + 1) + 2
        self.cheese_count = cheese_count
        self.maze = [
            [Cell(self.rng.get("cell")) for _ in range(self.width)] for _ in range(self.height)
        ]
        self.random_marker = [CHEESE for _ in range(cheese_count)] + [
            PATH for _ in range((self.width // 2) * (self.height // 2) - cheese_count)
        ]
        self.rng.get("map").shuffle(self.random_marker)

    def _is_within_bounds(self, x, y) -> bool:
        return 1 <= x < self.width - 1 and 1 <= y < self.height - 1

    def _get_neighbors(self, x, y, find_path=False) -> list[tuple[int, int]]:
        neighbors = []
        if find_path:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if find_path:
                if self._is_within_bounds(nx, ny) and self.maze[ny][nx].type > WALL:
                    neighbors.append((nx, ny))
            else:
                if self._is_within_bounds(nx, ny) and self.maze[ny][nx].type == WALL:
                    neighbors.append((nx, ny))
        return neighbors

    def generate_maze(self):
        self.gen_start_x, self.gen_start_y = (
            self.rng.get("map").integers(1, (self.width - 2) // 2) * 2 - 1,
            self.rng.get("map").integers(1, (self.height - 2) // 2) * 2 - 1,
        )
        self.start_x, self.start_y = (
            self.rng.get("position").integers(1, (self.width - 2) // 2) * 2 - 1,
            self.rng.get("position").integers(1, (self.height - 2) // 2) * 2 - 1,
        )
        self.maze[self.gen_start_y][self.gen_start_x].type = PATH
        stack = [(self.gen_start_x, self.gen_start_y)]

        while stack:
            x, y = stack[-1]
            neighbors = self._get_neighbors(x, y)
            if not neighbors:
                stack.pop()
                continue
            # next step
            nx: int
            ny: int
            nx, ny = self.rng.get("map").choice(neighbors)
            self.maze[ny][nx].type = self.random_marker.pop()

            self.maze[(ny + y) // 2][(nx + x) // 2].type = PATH
            stack.append((nx, ny))

            time.sleep(0.01)
            self.display_maze()

    def display_maze(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                back_color = None
                text = "   "
                if self.maze[y][x].type == WALL:
                    back_color = "on_white"
                    text = "   "
                elif self.maze[y][x].type == PATH:
                    back_color = (
                        get_on_color_by_visited_times(self.maze[y][x].data["visited_times"])
                        if self.maze[y][x].data["visited_times"]
                        else "on_black"
                    )
                    text = " " + (self.maze[y][x].data.get("random_code")) + " "

                elif self.maze[y][x].type == CHEESE:
                    text = "🧀 "
                    back_color = None  # or any default color you want
                string += colored(text, "white", back_color)
            string += "\n"
        print("\033[{0};{1}f{2}".format(0, 0, string))
        print("Start position: ", self.gen_start_x, self.gen_start_y)
        print("Key: ", self.sha_key)

    def put_letter(self, string: str):
        UP, RIGHT, DOWN, LEFT = [0, -1], [1, 0], [0, 1], [-1, 0]
        DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
        x, y = self.start_x, self.start_y
        current_direction = 0
        while True:
            right_direction = (current_direction + 1) % 4
            dx, dy = DIRECTIONS[right_direction]
            right_x, right_y = x + dx, y + dy
            if self.maze[right_y][right_x].type != WALL:
                # 右邊有路就往右轉
                current_direction = right_direction
                x, y = right_x, right_y
                self.maze[y][x].data["visited_times"] += 1
            else:
                # 右邊沒路
                dx, dy = DIRECTIONS[current_direction]
                next_x, next_y = x + dx, y + dy
                if self.maze[next_y][next_x].type != WALL:
                    # 前面有路前進
                    x, y = next_x, next_y
                    self.maze[y][x].data["visited_times"] += 1
                else:
                    # 死路鎖往左轉再重新檢測
                    current_direction = (current_direction - 1) % 4
            self.display_maze()


if __name__ == "__main__":
    # width = int(input("Enter maze width: "))
    # height = int(input("Enter maze height : "))
    # cheese_count = int(input("Enter number of cheeses: "))

    maze_generator = MazeGenerator(25, 25, 10, "")
    os.system("cls")
    maze_generator.generate_maze()
    maze_generator.display_maze()
    maze_generator.put_letter("Hello World")
