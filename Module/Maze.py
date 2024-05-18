from collections import defaultdict
import os
import string
from typing import TypedDict, List, Literal
import time
import hashlib
import numpy as np
from termcolor import colored

CHEESE, PATH, WALL = 2, 1, 0
codes = list(string.ascii_uppercase + string.digits + string.ascii_lowercase)

DEBUG = False


def _print(*args, **kwargs):
    global DEBUG
    if DEBUG:
        print(*args, **kwargs)


def ord_(char: str) -> int:
    return codes.index(char)


class CellData(TypedDict):
    visited_times: int
    random_code: str
    letters: List[str]


class Cell:
    def __init__(self, rng: np.random.Generator):
        self.type = WALL
        self.data: CellData = {
            "visited_times": 0,
            "random_code": rng.choice(codes),
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
    def __init__(self, width: int, height: int, cheese_count: int, key: str, debug=False):
        self.sha_key = int(hashlib.sha256(key.encode()).digest().hex(), 16)
        self.rng = {
            "map": np.random.default_rng(self.sha_key),
            "position": np.random.default_rng(self.sha_key + 1),
            "cell": np.random.default_rng(self.sha_key + 2),
            "direction": np.random.default_rng(self.sha_key + 3),
        }
        global DEBUG
        DEBUG = debug
        if DEBUG:
            os.system("cls")
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
        # return
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
        _print("\033[{0};{1}f{2}".format(0, 0, string))
        _print("Start position: ", self.gen_start_x, self.gen_start_y)
        _print("Key: ", self.sha_key)


class MazeSolver:
    x, y = 0, 0
    poops: list[str] = []

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
        self.poops.append(self.maze_generator.maze[y][x].data["random_code"])
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

    def run(self) -> str:
        if self.action == "encrypt":
            _print("Poops:", self.poops)
            table_encrypt = []
            cheese_index_map = defaultdict(lambda: 0)
            _print("對應表:")
            for i in range(len(self.cheese_points)):
                cheese_index_map[self.cheese_points[i]] += 1
                item = [
                    self.cheese_points[i],
                    self.strings[i],
                    self.maze_generator.maze[self.cheese_points[i][1]][
                        self.cheese_points[i][0]
                    ].data["random_code"],
                    cheese_index_map[self.cheese_points[i]],  # 每個Cheese的Letters排序用
                ]
                table_encrypt.append(item)
                _print(item)

            _print("換位表:")  # 先比 0 再比 1 在比 3
            sorted_table = sorted(table_encrypt, key=lambda x: (x[0][1], x[0][0], x[3]))
            for i in range(len(sorted_table)):
                _print(sorted_table[i])

            _print("和poop code相加:")
            for i in range(len(sorted_table)):
                sorted_table[i][1] = codes[
                    (ord_(sorted_table[i][1]) + (ord_(sorted_table[i][2]) * i)) % len(codes)
                ]
                _print(sorted_table[i])

            _print("和路上的大便攪和:")
            poopAverage = np.average(list(map(lambda x: ord_(x), self.poops)))
            poopStd = np.std(list(map(lambda x: ord_(x), self.poops)))
            for i in range(len(sorted_table)):
                after_pooped = (ord_(sorted_table[i][1]) + int(poopAverage)) % len(codes)
                after_pooped = (after_pooped + int(poopStd)) % len(codes)
                sorted_table[i][1] = codes[after_pooped]
                _print(sorted_table[i])
            _print("加密後的字串:", "".join(list(map(lambda x: x[1], sorted_table))))
            return "".join(list(map(lambda x: x[1], sorted_table)))
        elif self.action == "decrypt":
            table_decrypt = []
            cheese_index_map = defaultdict(lambda: 0)
            _print("對應表:")
            for i in range(len(self.cheese_points)):
                cheese_index_map[self.cheese_points[i]] += 1
                item = [
                    self.cheese_points[i],
                    self.strings[i],
                    self.maze_generator.maze[self.cheese_points[i][1]][
                        self.cheese_points[i][0]
                    ].data["random_code"],
                    cheese_index_map[self.cheese_points[i]],  # 每個Cheese的Letters排序用
                    i,  # 等等排回去用
                ]
                table_decrypt.append(item)
                _print(item)
            sorted_table = sorted(table_decrypt, key=lambda x: (x[0][1], x[0][0], x[3]))

            _print("放入加密字串:")
            for i in range(len(sorted_table)):
                sorted_table[i][1] = self.strings[i]
                _print(sorted_table[i])
            _print("和路上的大便攪和反向:")
            poopAverage = np.average(list(map(lambda x: ord_(x), self.poops)))
            poopStd = np.std(list(map(lambda x: ord_(x), self.poops)))
            for i in range(len(sorted_table)):
                before_pooped = (ord_(sorted_table[i][1]) - int(poopStd)) % len(codes)
                before_pooped = (before_pooped - int(poopAverage)) % len(codes)
                sorted_table[i][1] = codes[before_pooped]
                _print(sorted_table[i])

            _print("和poop code相加反向:")
            for i in range(len(sorted_table)):
                sorted_table[i][1] = codes[
                    (ord_(sorted_table[i][1]) - (ord_(sorted_table[i][2])) * i) % len(codes)
                ]
                _print(sorted_table[i])

            _print("排序回去:")
            sorted_table = sorted(sorted_table, key=lambda x: x[4])
            for i in range(len(sorted_table)):
                _print(sorted_table[i])

            _print("解密後的字串:", "".join(list(map(lambda x: x[1], sorted_table))))
            return "".join(list(map(lambda x: x[1], sorted_table)))

        else:
            raise ValueError("Invalid action")


if __name__ == "__main__":
    key = input("Enter key: ")
    input_msg = input("Enter message: ")
    maze = Maze(25, 25, 10, key, debug=False)
    _print("Key: ", key)
    os.system("pause")
    # os.system("cls")
    maze.generate_maze()
    maze.display_maze()
    solver = MazeSolver(maze, input_msg, "encrypt")
    solver.solve()
    encrypted_string = solver.run()
    print("\n\n三秒後開始解密")
    time.sleep(3)
    # os.system("cls")
    solver = MazeSolver(maze, encrypted_string, "decrypt")
    solver.solve()
    decrypted_string = solver.run()

    print("Encrypted string:", encrypted_string)
    print("Decrypted string:", decrypted_string)
