from EncryptAlgorithm import EncryptAlgorithm
import random

class MazeEncryption(EncryptAlgorithm):
    """
    Message = Hello

    Todo:
    1. 死路為放置明文的位置，按照順序放置(讀就從左上角開始讀取，往右讀取)
    2. 迷宮中有起司位置，碰到起司位置，改變老鼠規則
    3. 明文和明文之間的間格數，產生間隔數的亂數，  SECRET = l____o_____H_______l_e (假設H-e 間隔數為4， e-l 間隔數為5， l-l 間隔數為7，l-o 間隔數為1)
                                            這些亂數就像老鼠拉的poop
                                            key1 = ____
                                            key2 = _____
                                            key3 = _______
                                            key4 = _
    4. 那些大便，設第一個poopData為明文
       再加上該大便格子的位置(poopData_{i-1}+poopKey_{i}+y_{i}*cols+x_{i} % totalCols)，就是明文的要代換的位置，若位置為牆壁，則順時針往外旋轉找到第一個不為牆壁的位置
    """

    @staticmethod
    def generateKey(width: int = 10, height: int = 10):
        print("🔥[MazeAlg] Generating key...")
        # 初始化迷宮
        ...
        maze_str = '\n'.join(''.join(row) for row in maze)
        print("🔥[MazeAlg] Key generated.")
        print(maze_str)
        pass

    def decrypt(self, secret: str) -> str:
        pass

    def encrypt(self, message: str) -> str:
        pass


if __name__ == '__main__':
    maze = MazeEncryption(MazeEncryption.generateKey())
    print(maze.encrypt("Hello"))
    print(maze.decrypt("l____o_____H_______l_e"))
