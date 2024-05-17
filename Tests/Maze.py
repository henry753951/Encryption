from collections import defaultdict
import os
import string
from typing import TypedDict, List, Literal
import time
import hashlib
import numpy as np
from termcolor import colored

CHEESE, PATH, WALL = 2, 1, 0


class CellData(TypedDict):
    visited_times: int
    random_code: str
    letters: List[str]


class Cell:
    def __init__(self, rng: np.random.Generator):
        self.type = WALL
        self.data: CellData = {
            "visited_times": 0,
            "random_code": rng.choice(
                list(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            ),
            "letters": [],
        }


def get_on_color_by_visited_times(visited_times: int):
    visited_times = visited_times % 5
    if visited_times == 1:
        return "on_green"
    elif visited_times == 2:
        return "on_blue"
    elif visited_times == 3:
        return "on_magenta"
    elif visited_times == 4:
        return "on_cyan"
    else:
        return "on_red"


class Maze:
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

            # self.display_maze()

    def display_maze(self):
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                back_color = None
                text = "   "
                if self.maze[y][x].type != WALL:
                    back_color = (
                        get_on_color_by_visited_times(self.maze[y][x].data["visited_times"])
                        if self.maze[y][x].data["visited_times"]
                        else "on_black"
                    )
                if self.maze[y][x].type == WALL:
                    back_color = "on_white"
                    text = "   "
                elif self.maze[y][x].type == PATH:
                    text = " " + (self.maze[y][x].data["random_code"]) + " "
                elif self.maze[y][x].type == CHEESE:
                    text = "🧀"
                    if self.maze[y][x].data["letters"]:
                        text += self.maze[y][x].data["letters"][-1]
                        text = "\033[1m" + text + "\033[0m"
                    else:
                        text += " "

                string += colored(text, "white", back_color)
            string += "\n"
        print("\033[{0};{1}f{2}".format(0, 0, string))
        print("Start position: ", self.gen_start_x, self.gen_start_y)
        print("Key: ", self.sha_key)


class MazeSolver:
    x, y = 0, 0

    def __init__(self, maze_generator: Maze, string: str, action: Literal["encrypt", "decrypt"]):
        self.maze_generator = maze_generator
        self.start_x = maze_generator.start_x
        self.start_y = maze_generator.start_y
        self.strings = list(string)
        #
        self.temp_count = len(self.strings)
        self.cheese_points: List[tuple[int, int]] = []
        self.action = action

    def solve(self):
        UP, RIGHT, DOWN, LEFT = [0, -1], [1, 0], [0, 1], [-1, 0]
        DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
        self.x, self.y = self.start_x, self.start_y
        current_direction = 0
        temp_string = self.strings.copy()
        while True:
            right_direction = (current_direction + 1) % 4
            dx, dy = DIRECTIONS[right_direction]
            right_x, right_y = self.x + dx, self.y + dy
            if self.maze_generator.maze[right_y][right_x].type != WALL:
                # 右邊有路就往右轉
                current_direction = right_direction
                if not self.move(right_x, right_y, temp_string):
                    break
            else:
                # 右邊沒路
                dx, dy = DIRECTIONS[current_direction]
                next_x, next_y = self.x + dx, self.y + dy
                if self.maze_generator.maze[next_y][next_x].type != WALL:
                    # 前面有路前進
                    if not self.move(next_x, next_y, temp_string):
                        break
                else:
                    # 死路鎖往左轉再重新檢測
                    current_direction = (current_direction - 1) % 4
            self.maze_generator.display_maze()

    def move(self, x: int, y: int, temp_string: list[str]) -> bool:
        self.x, self.y = x, y
        self.maze_generator.maze[y][x].data["visited_times"] += 1
        if self.maze_generator.maze[y][x].type == CHEESE:
            if self.temp_count:
                self.temp_count -= 1
                self.cheese_points.append((x, y))
                self.do_cheese(x, y, temp_string, self.action)
            else:
                return False  # 沒有字母了
        return True

    def do_cheese(
        self, x: int, y: int, temp_string: list[str], action: Literal["encrypt", "decrypt"]
    ):
        if action == "encrypt":
            self.maze_generator.maze[y][x].data["letters"].append(temp_string.pop(0))
        elif action == "decrypt":
            pass
        else:
            raise ValueError("Invalid action")

    def run(self):
        self.solve()
        table_encrypt = []
        cheese_index_map = defaultdict(lambda: 0)
        print("對應表:")
        for i in range(len(self.cheese_points)):
            cheese_index_map[self.cheese_points[i]] += 1
            item = (
                self.cheese_points[i],
                self.strings[i],
                self.maze_generator.maze[self.cheese_points[i][1]][self.cheese_points[i][0]].data[
                    "random_code"
                ],
                cheese_index_map[self.cheese_points[i]],
            )
            table_encrypt.append(item)
            print(item)

        print("換位表:")  # 先比 0 再比 1 在比 3
        sorted_table = sorted(table_encrypt, key=lambda x: (x[0][1], x[0][0], x[3]))
        for i in range(len(sorted_table)):
            print(sorted_table[i])


if __name__ == "__main__":
    # width = int(input("Enter maze width: "))
    # height = int(input("Enter maze height : "))
    # cheese_count = int(input("Enter number of cheeses: "))

    maze = Maze(25, 25, 10, "")
    os.system("cls")
    maze.generate_maze()
    maze.display_maze()
    solver = MazeSolver(maze, "HelloWorld", "encrypt")
    solver.run()
