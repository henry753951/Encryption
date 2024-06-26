from BaseEncryptAlgorithm import EncryptAlgorithm
from Module.Maze import Maze, MazeSolver

class MazeEncryption(EncryptAlgorithm):
    def __init__(self, secret_key: str, options: dict = {}) -> None:
        super().__init__(secret_key)
        width = options.get("width", 10)
        height = options.get("height", 10)
        cheese = options.get("cheese", 5)
        debug = options.get("debug", False)

        self.maze = Maze(width, height, cheese, secret_key, debug)
        self.maze.generate_maze()

    def decrypt(self, secret: str) -> str:
        solver = MazeSolver(self.maze, secret, "decrypt")
        solver.solve()
        return solver.run()

    def encrypt(self, message: str) -> str:
        solver = MazeSolver(self.maze, message, "encrypt")
        solver.solve()
        return solver.run()
