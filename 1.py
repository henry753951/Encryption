import random

def generate_sequence(seed, length):
    random.seed(seed)  # 設置隨機種子
    sequence = []
    for _ in range(length):
        choice = random.choice([0, 1, 2, 3])  # 從 [0, 1, 2, 3] 中隨機選擇一個數字
        sequence.append(choice)
    return sequence

seed = "ABSDx"  # 固定種子
length = 10  # 生成序列的長度
generated_sequence = generate_sequence(seed, length)
print(generated_sequence)